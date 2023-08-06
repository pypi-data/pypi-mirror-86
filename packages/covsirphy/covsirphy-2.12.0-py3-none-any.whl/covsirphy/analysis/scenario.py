#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import numpy as np
import pandas as pd
from covsirphy.util.error import deprecate
from covsirphy.util.plotting import line_plot, box_plot
from covsirphy.cleaning.term import Term
from covsirphy.cleaning.jhu_data import JHUData
from covsirphy.cleaning.population import PopulationData
from covsirphy.phase.phase_unit import PhaseUnit
from covsirphy.phase.phase_series import PhaseSeries
from covsirphy.analysis.param_tracker import ParamTracker


class Scenario(Term):
    """
    Scenario analysis.

    Args:
        jhu_data (covsirphy.JHUData): object of records
        population_data (covsirphy.PopulationData): PopulationData object
        country (str): country name
        province (str or None): province name
        tau (int or None): tau value
        auto_complement (bool): if True, the number of cases will be complemented.
    """

    def __init__(self, jhu_data, population_data, country, province=None, tau=None, auto_complement=True):
        # Population
        population_data = self.ensure_instance(
            population_data, PopulationData, name="population_data")
        self.population = population_data.value(country, province=province)
        # Records
        self.jhu_data = self.ensure_instance(
            jhu_data, JHUData, name="jhu_data")
        # Area name
        self.country = country
        self.province = province or self.UNKNOWN
        self.area = JHUData.area_name(country, province)
        # tau value must be shared
        self.tau = self.ensure_tau(tau)
        # Whether complement the number of cases or not
        self._auto_complement = bool(auto_complement)
        self._complemented = False
        # Create {scenario_name: PhaseSeries} and set records
        self.record_df = pd.DataFrame()
        self._first_date = None
        self._last_date = None
        self._init_phase_series()

    def __getitem__(self, key):
        if key in self._series_dict:
            return self._series_dict[key]
        raise KeyError(f"{key} scenario is not registered.")

    def __setitem__(self, key, value):
        self.ensure_instance(value, PhaseSeries, name="value")
        self._series_dict[key] = value

    def _init_phase_series(self):
        """
        Initialize dictionary of phase series and set records.
        Only when auto-complement mode, complement records if necessary.
        """
        # Set records (complement records, if necessary)
        if self._auto_complement:
            self.complement()
            if self.record_df.empty:
                self.complement_reverse()
        else:
            self.complement_reverse()
        if self.record_df.empty:
            area = self.jhu_data.area_name(
                self.country, province=self.province)
            raise ValueError(
                f"Records with 'Recovered > 0' in {area} are un-registered.")
        # First/last date of the records
        if self._first_date is None:
            series = self.record_df.loc[:, self.DATE]
            self._first_date = series.min().strftime(self.DATE_FORMAT)
            self._last_date = series.max().strftime(self.DATE_FORMAT)
        # Set main scenario
        self._series_dict = {
            self.MAIN: PhaseSeries(
                self._first_date, self._last_date, self.population
            )
        }

    def complement(self, interval=2, max_ignored=100):
        """
        Complement the number of recovered cases when not updated/reported.

        Args:
            interval (int): expected update interval of the number of recovered cases [days]
            max_ignored (int): Max number of recovered cases to be ignored [cases]

        Returns:
            covsirphy.Scenario: self

        Notes:
            If the number of recovered cases did not change
            for more than @interval days after reached @max_ignored cases,
            complement will be applied to the number of recovered cases.
        """
        self.record_df, self._complemented = self.jhu_data.subset_complement(
            country=self.country, province=self.province,
            start_date=self._first_date, end_date=self._last_date, population=self.population,
            interval=interval, max_ignored=max_ignored)
        return self

    def complement_reverse(self):
        """
        Restore the raw records. Reverse method of covsirphy.Scenario.complement().

        Returns:
            covsirphy.Scenario: self
        """
        self.record_df = self.jhu_data.subset(
            country=self.country,
            province=self.province,
            start_date=self._first_date,
            end_date=self._last_date,
            population=self.population
        )
        self._complemented = False
        return self

    @property
    def first_date(self):
        """
        str: the first date of the records
        """
        return self._first_date

    @first_date.setter
    def first_date(self, date):
        self.ensure_date_order(self._first_date, date, name="date")
        self.ensure_date_order(date, self._last_date, name="date")
        self._first_date = date
        self._init_phase_series()

    @property
    def last_date(self):
        """
        str: the last date of the records
        """
        return self._last_date

    @last_date.setter
    def last_date(self, date):
        self.ensure_date_order(self._first_date, date, name="date")
        self.ensure_date_order(date, self._last_date, name="date")
        self._last_date = date
        self._init_phase_series()

    def records(self, show_figure=True, filename=None):
        """
        Return the records as a dataframe.

        Args:
            show_figure (bool): if True, show the records as a line-plot.
            filename (str): filename of the figure, or None (show figure)

        Returns:
            pandas.DataFrame
                Index:
                    reset index
                Columns:
                    - Date (pd.TimeStamp): Observation date
                    - Confirmed (int): the number of confirmed cases
                    - Infected (int): the number of currently infected cases
                    - Fatal (int): the number of fatal cases
                    - Recovered (int): the number of recovered cases (> 0)

        Notes:
            Records with Recovered > 0 will be selected.
            If complement was performed by Scenario.complement() or Scenario(auto_complement=True),
            "(complemented)" will be added to the title of the figure.
        """
        df = self.record_df.drop(self.S, axis=1)
        if not show_figure:
            return df
        title = f"{self.area}: Cases over time{' (complemented)' if self._complemented else ''}"
        line_plot(
            df.set_index(self.DATE).drop(self.C, axis=1),
            title,
            y_integer=True,
            filename=filename
        )
        return df

    def _create_tracker(self, name):
        """
        Create a instance of covsirphy.ParamTracker.

        Args:
            name (str): scenario name

        Returns:
            covsirphy.ParamTracker
        """
        return ParamTracker(
            record_df=self.record_df, phase_series=self._ensure_name(name),
            area=self.area, tau=self.tau)

    @deprecate(old="Scenario.add_phase()", new="Scenario.add()")
    def add_phase(self, **kwargs):
        return self.add(**kwargs)

    def add(self, name="Main", end_date=None, days=None,
            population=None, model=None, **kwargs):
        """
        Add a new phase.
        The start date will be the next date of the last registered phase.

        Args:
            name (str): phase series name, 'Main' or user-defined name
            end_date (str): end date of the new phase
            days (int): the number of days to add
            population (int or None): population value of the start date
            model (covsirphy.ModelBase or None): ODE model
            kwargs: keyword arguments of ODE model parameters, not including tau value.

        Returns:
            covsirphy.Scenario: self

        Notes:
            - If the phases series has not been registered, new phase series will be created.
            - Either @end_date or @days must be specified.
            - If @end_date and @days are None, the end date will be the last date of the records.
            - If both of @end_date and @days were specified, @end_date will be used.
            - If @popultion is None, initial value will be used.
            - If @model is None, the model of the last phase will be used.
            - Tau will be fixed as the last phase's value.
            - kwargs: Default values are the parameter values of the last phase.
        """
        series = self._ensure_name(name)
        try:
            self._series_dict[name].add(
                end_date=end_date, days=days, population=population,
                model=model, tau=self.tau, **kwargs
            )
        except ValueError:
            last_date = series.unit("last").end_date
            s1 = f'For "{name}" scenario, @end_date needs to match "DDMmmYYYY" format'
            raise ValueError(
                f'{s1} and be over {last_date}. However, {end_date} was applied.') from None
        return self

    def _ensure_name(self, name, template="Main"):
        """
        Ensure that the phases series is registered.
        If not registered, copy the template phase series.

        Args:
            name (str): phase series name
            template (str): name of template phase series
        """
        if name in self._series_dict.keys():
            return self._series_dict[name]
        # Phase series
        if template not in self._series_dict:
            raise KeyError(f"Template scenario {template} does not exist.")
        series = copy.deepcopy(self._series_dict[template])
        self._series_dict[name] = series
        return series

    def clear(self, name="Main", include_past=False, template="Main"):
        """
        Clear phase information.

        Args:
            name (str): phase series name
                - if 'Main', main phase series will be used
                - if not registered, new phaseseries will be created
            include_past (bool):
                - if True, include past phases.
                - future phase are always included
            template (str): name of template phase series

        Returns:
            covsirphy.Scenario: self
        """
        self._ensure_name(name, template=template)
        self._series_dict[name].clear(include_past=include_past)
        return self

    def _delete_series(self, name):
        """
        Delete a phase series.

        Args:
            name (str): name of phase series

        Returns:
            covsirphy.Scenario: self
        """
        if name == self.MAIN:
            self.clear(name=name, include_past=True)
            return self
        self._series_dict.pop(name)
        return self

    def delete(self, phases=None, name="Main"):
        """
        Delete phases.

        Args:
            phase (list[str] or None): phase names, or ['last']
            name (str): name of phase series

        Returns:
            covsirphy.Scenario: self

        Notes:
            If @phases is None, the phase series will be deleted.
            When @phase is '0th', disable 0th phase. 0th phase will not be deleted.
            If the last phase is included in @phases, the dates will be released from phases.
            If the last phase is not included, the dates will be assigned to the previous phase.
        """
        self._ensure_name(name)
        # Clear main series or delete sub phase series
        if phases is None:
            return self._delete_series(name)
        # Delete phases
        if not isinstance(phases, list):
            raise TypeError("@phases mut be a list of phase names.")
        phases = list(set(phases))
        if "last" in phases:
            self._series_dict[name].delete("last")
            phases.remove("last")
        phases = sorted(phases, key=self.str2num, reverse=True)
        for phase in phases:
            self._series_dict[name].delete(phase)
        return self

    def disable(self, phases, name="Main"):
        """
        The phases will be disabled and removed from summary.

        Args:
            phase (list[str] or None): phase names
            name (str): name of phase series

        Returns:
            covsirphy.Scenario: self
        """
        tracker = self._create_tracker(name)
        self._series_dict[name] = tracker.disable(phases)
        return self

    def enable(self, phases, name="Main"):
        """
        The phases will be enabled and appear in summary.

        Args:
            phase (list[str] or None): phase names
            name (str): name of phase series

        Returns:
            covsirphy.Scenario: self
        """
        tracker = self._create_tracker(name)
        self._series_dict[name] = tracker.enable(phases)
        return self

    def combine(self, phases, name="Main", population=None, **kwargs):
        """
        Combine the sequential phases as one phase.
        New phase name will be automatically determined.

        Args:
            phases (list[str]): list of phases
            name (str, optional): name of phase series
            population (int): population value of the start date
            kwargs: keyword arguments to save as phase information

        Raises:
            TypeError: @phases is not a list

        Returns:
            covsirphy.Scenario: self
        """
        series = self._ensure_name(name)
        # Sort and check @phase is a list
        if not isinstance(phases, list):
            raise TypeError("@phases must be a list of phase names.")
        phases = list(set(phases))
        if "last" in phases:
            last_phase = "last"
            phases.remove("last")
            phases = sorted(phases, key=self.str2num, reverse=False)
        else:
            phases = sorted(phases, key=self.str2num, reverse=False)
            last_phase = phases[-1]
        # Setting of the new phase
        start_date = series.unit(phases[0]).start_date
        end_date = series.unit(last_phase).end_date
        population = population or series.unit(last_phase).population
        new_unit = PhaseUnit(start_date, end_date, population)
        new_unit.set_ode(**kwargs)
        # Phases to keep
        kept_units = [
            unit for unit in series if unit < start_date or unit > end_date]
        # Replace units
        self._series_dict[name].replaces(
            phase=None, new_list=kept_units + [new_unit], keep_old=False)
        return self

    def separate(self, date, name="Main", population=None, **kwargs):
        """
        Create a new phase with the change point.
        New phase name will be automatically determined.

        Args:
            date (str): change point, i.e. start date of the new phase
            name (str): scenario name
            population (int): population value of the change point
            kwargs: keyword arguments of PhaseUnit.set_ode() if update is necessary

        Returns:
            covsirphy.Scenario: self
        """
        tracker = self._create_tracker(name)
        self._series_dict[name] = tracker.separate(
            date, population=population, **kwargs)
        return self

    def _summary(self, name=None):
        """
        Summarize the series of phases and return a dataframe.

        Args:
            name (str): phase series name
                - name of alternative phase series registered by Scenario.add()
                - if None, all phase series will be shown

        Returns:
            pandas.DataFrame:
            - if @name not None, as the same as PhaseSeries().summary()
            - if @name is None, index will be phase series name and phase name

        Notes:
            If 'Main' was used as @name, main PhaseSeries will be used.
        """
        if name is None:
            if len(self._series_dict.keys()) > 1:
                dataframes = []
                for (_name, series) in self._series_dict.items():
                    summary_df = series.summary()
                    summary_df = summary_df.rename_axis(self.PHASE)
                    summary_df[self.SERIES] = _name
                    dataframes.append(summary_df.reset_index())
                df = pd.concat(dataframes, ignore_index=True, sort=False)
                return df.set_index([self.SERIES, self.PHASE])
            name = self.MAIN
        series = self._ensure_name(name)
        return series.summary()

    def summary(self, columns=None, name=None):
        """
        Summarize the series of phases and return a dataframe.

        Args:
            name (str): phase series name
                - name of alternative phase series registered by Scenario.add()
                - if None, all phase series will be shown
            columns (list[str] or None): columns to show

        Returns:
            pandas.DataFrame:
            - if @name not None, as the same as PhaseSeries().summary()
            - if @name is None, index will be phase series name and phase name

        Notes:
            If 'Main' was used as @name, main PhaseSeries will be used.
            If @columns is None, all columns will be shown.
        """
        df = self._summary(name=name)
        all_cols = df.columns.tolist()
        if set(self.EST_COLS).issubset(all_cols):
            all_cols = [col for col in all_cols if col not in self.EST_COLS]
            all_cols += self.EST_COLS
        columns = columns or all_cols
        if not isinstance(columns, list):
            raise TypeError("@columns must be None or a list of strings.")
        if not set(columns).issubset(df.columns):
            raise KeyError(
                f"Un-registered columns were selected as @columns. Please use {', '.join(df.columns)}."
            )
        df = df.loc[:, columns]
        return df.dropna(how="all", axis=1).fillna(self.UNKNOWN)

    def trend(self, force=True, name="Main", show_figure=True, filename=None, **kwargs):
        """
        Perform S-R trend analysis and set phases.

        Args:
            force (bool): if True, change points will be over-written
            name (str): phase series name
            show_figure (bool): if True, show the result as a figure
            filename (str): filename of the figure, or None (display)
            kwargs: keyword arguments of ChangeFinder()

        Returns:
            covsirphy.Scenario: self
        """
        # Arguments
        if "n_points" in kwargs.keys():
            raise ValueError(
                "@n_points argument is un-necessary"
                " because the number of change points will be automatically determined."
            )
        try:
            include_init_phase = kwargs.pop("include_init_phase")
        except KeyError:
            include_init_phase = True
        try:
            force = kwargs.pop("set_phases")
        except KeyError:
            pass
        # S-R trend analysis
        tracker = self._create_tracker(name)
        self._series_dict[name] = tracker.trend(
            force=force, show_figure=show_figure, filename=filename, **kwargs)
        # Disable 0th phase, if necessary
        if not include_init_phase:
            self._series_dict[name].disable("0th")
        return self

    def estimate(self, model, phases=None, name="Main", n_jobs=-1, **kwargs):
        """
        Perform parameter estimation for each phases.

        Args:
            model (covsirphy.ModelBase): ODE model
            phases (list[str]): list of phase names, like 1st, 2nd...
            name (str): phase series name
            n_jobs (int): the number of parallel jobs or -1 (CPU count)
            kwargs: keyword arguments of model parameters and covsirphy.Estimator.run()

        Notes:
            - If 'Main' was used as @name, main PhaseSeries will be used.
            - If @name phase was not registered, new PhaseSeries will be created.
            - If @phases is None, all past phase will be used.
            - Phases with estimated parameter values will be ignored.
            - In kwargs, tau value cannot be included.
        """
        if self.TAU in kwargs:
            raise ValueError(
                "@tau must be specified when scenario = Scenario(), and cannot be specified here.")
        tracker = self._create_tracker(name)
        self.tau, self._series_dict[name] = tracker.estimate(
            model=model, phases=phases, n_jobs=n_jobs, **kwargs)

    def phase_estimator(self, phase, name="Main"):
        """
        Return the estimator of the phase.

        Args:
            phase (str): phase name, like 1st, 2nd...
            name (str): phase series name

        Return:
            covsirphy.Estimator: estimator of the phase
        """
        estimator = self._series_dict[name].unit(phase).estimator
        if estimator is None:
            raise AttributeError(
                f'Scenario.estimate(model, phases=["{phase}"], name={name}) must be done in advance.'
            )
        return estimator

    def estimate_history(self, phase, name="Main", **kwargs):
        """
        Show the history of optimization.

        Args:
            phase (str): phase name, like 1st, 2nd...
            name (str): phase series name
            kwargs: keyword arguments of covsirphy.Estimator.history()

        Notes:
            If 'Main' was used as @name, main PhaseSeries will be used.
        """
        estimator = self.phase_estimator(phase=phase, name=name)
        estimator.history(**kwargs)

    def estimate_accuracy(self, phase, name="Main", **kwargs):
        """
        Show the accuracy as a figure.

        Args:
            phase (str): phase name, like 1st, 2nd...
            name (str): phase series name
            kwargs: keyword arguments of covsirphy.Estimator.accuracy()

        Notes:
            If 'Main' was used as @name, main PhaseSeries will be used.
        """
        estimator = self.phase_estimator(phase=phase, name=name)
        estimator.accuracy(**kwargs)

    def simulate(self, name="Main", y0_dict=None, show_figure=True, filename=None):
        """
        Simulate ODE models with set/estimated parameter values and show it as a figure.

        Args:
            name (str): phase series name. If 'Main', main PhaseSeries will be used
            y0_dict(dict[str, float] or None): dictionary of initial values of variables
            show_figure (bool): if True, show the result as a figure
            filename (str): filename of the figure, or None (show figure)

        Returns:
            pandas.DataFrame
                Index:
                    reset index
                Columns:
                    - Date (pd.TimeStamp): Observation date
                    - Country (str): country/region name
                    - Province (str): province/prefecture/state name
                    - Variables of the model and dataset (int): Confirmed etc.
        """
        tracker = self._create_tracker(name)
        try:
            sim_df = tracker.simulate(y0_dict=y0_dict)
        except ValueError:
            raise ValueError(
                "Phases should be registered with Scenario.trend() or Scenario.add() in advance.") from None
        except NameError:
            raise NameError(
                "Parameter estimation should be done with Scenario.estimate() in advance.") from None
        if not show_figure:
            return sim_df
        # Show figure
        df = sim_df.set_index(self.DATE)
        fig_cols_set = set(df.columns) & set(self.FIG_COLUMNS)
        fig_cols = [col for col in self.FIG_COLUMNS if col in fig_cols_set]
        line_plot(
            df[fig_cols],
            title=f"{self.area}: Simulated number of cases ({name} scenario)",
            filename=filename,
            y_integer=True,
            v=tracker.change_dates()
        )
        return sim_df

    def get(self, param, phase="last", name="Main"):
        """
        Get the parameter value of the phase.

        Args:
            param (str): parameter name (columns in self.summary())
            phase (str): phase name or 'last'
                - if 'last', the value of the last phase will be returned
            name (str): phase series name

        Returns:
            str or int or float

        Notes:
            If 'Main' was used as @name, main PhaseSeries will be used.
        """
        df = self._ensure_name(name).summary()
        if param not in df.columns:
            raise KeyError(f"@param must be in {', '.join(df.columns)}.")
        if phase == "last":
            phase = df.index[-1]
        return df.loc[phase, param]

    def _param_history(self, targets, name):
        """
        Return the subset of summary dataframe to select the target of parameter history.

        Args:
            targets (list[str] or str): parameters to show (Rt etc.)
            name (str): phase series name

        Returns:
            pandas.DataFrame: selected summary dataframe

        Raises:
            KeyError: targets are not in the columns of summary dataframe
        """
        series = self._series_dict[name]
        model_set = {unit.model for unit in series}
        model_set = model_set - set([None])
        parameters = self.flatten([m.PARAMETERS for m in model_set])
        day_params = self.flatten([m.DAY_PARAMETERS for m in model_set])
        selectable_cols = [self.N, *parameters, self.RT, *day_params]
        selectable_set = set(selectable_cols)
        df = series.summary().replace(self.UNKNOWN, None)
        if not selectable_set.issubset(df.columns):
            raise ValueError(
                f"Scenario.estimate(model, phases=None, name={name}) must be done in advance.")
        targets = [targets] if isinstance(targets, str) else targets
        targets = targets or selectable_cols
        if not set(targets).issubset(selectable_set):
            raise KeyError(
                f"@targets must be selected from {', '.join(selectable_cols)}."
            )
        df = df.loc[:, targets].dropna(how="any", axis=0)
        return df.astype(np.float64)

    @deprecate(
        old="Scenario.param_history(targets: list)",
        new="Scenario.history(target: str)",
        version="2.7.3-alpha")
    def param_history(self, targets=None, name="Main", divide_by_first=True,
                      show_figure=True, filename=None, show_box_plot=True, **kwargs):
        """
        Return subset of summary and show a figure to show the history.

        Args:
            targets (list[str] or str): parameters to show (Rt etc.)
            name (str): phase series name
            divide_by_first (bool): if True, divide the values by 1st phase's values
            show_box_plot (bool): if True, box plot. if False, line plot
            show_figure (bool): If True, show the result as a figure
            filename (str): filename of the figure, or None (show figure)
            kwargs: keyword arguments of pd.DataFrame.plot or line_plot()

        Returns:
            pandas.DataFrame

        Notes:
            If 'Main' was used as @name, main PhaseSeries will be used.
        """
        self._ensure_name(name)
        # Select target to show
        df = self._param_history(targets, name)
        # Divide by the first phase parameters
        if divide_by_first:
            df = df / df.iloc[0, :]
            title = f"{self.area}: Ratio to 1st phase parameters ({name} scenario)"
        else:
            title = f"{self.area}: History of parameter values ({name} scenario)"
        if not show_figure:
            return df
        if show_box_plot:
            h_values = [1.0] if divide_by_first or self.RT in targets else None
            box_plot(df, title, h=h_values, filename=filename)
            return df
        _df = df.reset_index(drop=True)
        _df.index = _df.index + 1
        h = 1.0 if divide_by_first else None
        line_plot(
            _df, title=title,
            xlabel="Phase", ylabel=str(), math_scale=False, h=h,
            filename=filename
        )
        return df

    def _describe(self, y0_dict=None):
        """
        Describe representative values.

        Args:
            y0_dict (dict or None): dictionary of initial values or None
                - key (str): variable name
                - value (float): initial value

        Returns:
            pandas.DataFrame
                Index:
                    (int): scenario name
                Columns:
                    - max(Infected): max value of Infected
                    - argmax(Infected): the date when Infected shows max value
                    - Confirmed({date}): Confirmed on the next date of the last phase
                    - Infected({date}): Infected on the next date of the last phase
                    - Fatal({date}): Fatal on the next date of the last phase
        """
        _dict = {}
        for (name, _) in self._series_dict.items():
            # Predict the number of cases
            df = self.simulate(name=name, y0_dict=y0_dict, show_figure=False)
            df = df.set_index(self.DATE)
            cols = df.columns[:]
            last_date = df.index[-1]
            # Max value of Infected
            max_ci = df[self.CI].max()
            argmax_ci = df[self.CI].idxmax().strftime(self.DATE_FORMAT)
            # Confirmed on the next date of the last phase
            last_c = df.loc[last_date, self.C]
            # Infected on the next date of the last phase
            last_ci = df.loc[last_date, self.CI]
            # Fatal on the next date of the last phase
            last_f = df.loc[last_date, self.F] if self.F in cols else None
            # Save representative values
            last_date_str = last_date.strftime(self.DATE_FORMAT)
            _dict[name] = {
                f"max({self.CI})": max_ci,
                f"argmax({self.CI})": argmax_ci,
                f"{self.C} on {last_date_str}": last_c,
                f"{self.CI} on {last_date_str}": last_ci,
                f"{self.F} on {last_date_str}": last_f,
            }
        return pd.DataFrame.from_dict(_dict, orient="index")

    def describe(self, y0_dict=None, with_rt=True):
        """
        Describe representative values.

        Args:
            y0_dict (dict or None): dictionary of initial values or None
                - key (str): variable name
                - value (float): initial value
            with_rt (bool): whether show the history of Rt values

        Returns:
            pandas.DataFrame:
                Index:
                    str: scenario name
                Columns:
                    - max(Infected): max value of Infected
                    - argmax(Infected): the date when Infected shows max value
                    - Confirmed({date}): Confirmed on the next date of the last phase
                    - Infected({date}): Infected on the next date of the last phase
                    - Fatal({date}): Fatal on the next date of the last phase
                    - nth_Rt etc.: Rt value if the values are not the same values
        """
        df = self._describe(y0_dict=y0_dict)
        if not with_rt or len(self._series_dict) == 1:
            return df
        # History of reproduction number
        rt_df = self.summary().reset_index()
        rt_df = rt_df.pivot_table(
            index=self.SERIES, columns=self.PHASE, values=self.RT)
        rt_df = rt_df.fillna(self.UNKNOWN)
        rt_df = rt_df.loc[:, rt_df.nunique() > 1]
        cols = sorted(rt_df, key=self.str2num)
        return df.join(rt_df[cols].add_suffix(f"_{self.RT}"), how="left")

    def _track_param(self, name):
        """
        Get the history of parameters for the scenario.

        Args:
            name (str): phase series name

        Returns:
            pandas.DataFrame:
                Index: Date (pandas.TimeStamp)
                Columns:
                    - Population (int)
                    - Rt (float)
                    - parameter values (float)
                    - day parameter values (float)
        """
        df = self.summary(name=name).replace(self.UNKNOWN, None)
        if self.ODE not in df.columns:
            raise ValueError(
                f"Scenario.estimate(model, name={name}) must be done in advance.")
        # Date range to dates
        df[self.START] = pd.to_datetime(df[self.START])
        df[self.END] = pd.to_datetime(df[self.END])
        df[self.DATE] = df[[self.START, self.END]].apply(
            lambda x: pd.date_range(x[0], x[1]).tolist(), axis=1)
        df = df.reset_index(drop=True).explode(self.DATE)
        # Columns
        df = df.drop(
            [self.TENSE, self.START, self.END, self.ODE, self.TAU, *self.EST_COLS],
            axis=1, errors="ignore")
        df = df.set_index(self.DATE)
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df[self.N] = df[self.N].astype(np.int64)
        return df

    def _track(self, name, y0_dict=None):
        """
        Show values of parameters and variables in one dataframe for the scenario.

        Args:
            name (str): phase series name
            y0_dict (dict or None): dictionary of initial values or None
                - key (str): variable name
                - value (float): initial value

        Returns:
            pandas.DataFrame:
                Index: reset index
                Columns:
                    - Date (pandas.TimeStamp)
                    - variables (int)
                    - Population (int)
                    - Rt (float)
                    - parameter values (float)
                    - day parameter values (float)
        """
        sim_df = self.simulate(name=name, y0_dict=y0_dict, show_figure=False)
        param_df = self._track_param(name=name)
        return pd.merge(
            sim_df, param_df, how="inner",
            left_on=self.DATE, right_index=True, sort=True
        )

    def track(self, with_actual=True, y0_dict=None):
        """
        Show values of parameters and variables in one dataframe.

        Args:
            with_actual (bool): if True, show actual number of cases will included as "Actual" scenario
            y0_dict (dict or None): dictionary of initial values or None
                - key (str): variable name
                - value (float): initial value

        Returns:
            pandas.DataFrame:
                Index: reset index
                Columns:
                    - Scenario (str)
                    - Date (pandas.TimeStamp)
                    - variables (int)
                    - Population (int)
                    - Rt (float)
                    - parameter values (float)
                    - day parameter values (float)
        """
        dataframes = []
        append = dataframes.append
        for name in self._series_dict.keys():
            df = self._track(name=name, y0_dict=y0_dict)
            df.insert(0, self.SERIES, name)
            append(df)
        if with_actual:
            df = self.records(show_figure=False)
            df.insert(0, self.SERIES, self.ACTUAL)
            append(df)
        return pd.concat(dataframes, axis=0, sort=False)

    def _history(self, target, with_actual=True, y0_dict=None):
        """
        Show the history of variables and parameter values to compare scenarios.

        Args:
            target (str): parameter or variable name to show (Rt, Infected etc.)
            with_actual (bool): if True and @target is a variable name, show actual number of cases
            y0_dict (dict or None): dictionary of initial values or None
                - key (str): variable name
                - value (float): initial value

        Returns:
            pandas.DataFrame
        """
        # Include actual data or not
        with_actual = with_actual and target in self.VALUE_COLUMNS
        # Get tracking data
        df = self.track(with_actual=with_actual, y0_dict=y0_dict)
        if target not in df.columns:
            col_str = ", ".join(list(df.columns))
            raise KeyError(
                f"@target must be selected from {col_str}, but {target} was applied.")
        # Select the records of target variable
        return df.pivot_table(
            values=target, index=self.DATE, columns=self.SERIES, aggfunc="last")

    def history(self, target, with_actual=True, y0_dict=None, show_figure=True, filename=None):
        """
        Show the history of variables and parameter values to compare scenarios.

        Args:
            target (str): parameter or variable name to show (Rt, Infected etc.)
            with_actual (bool): if True and @target is a variable name, show actual number of cases
            y0_dict (dict or None): dictionary of initial values or None
                - key (str): variable name
                - value (float): initial value
            show_figure (bool): If True, show the result as a figure
            filename (str): filename of the figure, or None (show figure)

        Returns:
            pandas.DataFrame
        """
        df = self._history(
            target=target, with_actual=with_actual, y0_dict=y0_dict)
        if not show_figure:
            return df
        if target == self.RT:
            ylabel = self.RT_FULL
        elif target in self.VALUE_COLUMNS:
            ylabel = f"The number of {target.lower()} cases"
        else:
            ylabel = target
        title = f"{self.area}: {ylabel} over time"
        tracker = self._create_tracker(self.MAIN)
        line_plot(
            df, title, ylabel=ylabel,
            h=1.0 if target == self.RT else None,
            v=tracker.change_dates(),
            math_scale=False,
            filename=filename
        )
        return df

    def history_rate(self, params=None, name="Main", show_figure=True, filename=None):
        """
        Show change rates of parameter values in one figure.
        We can find the parameters which increased/decreased significantly.

        Args:
            params (list[str] or None): parameters to show
            name (str): phase series name
            show_figure (bool): If True, show the result as a figure
            filename (str): filename of the figure, or None (show figure)

        Returns:
            pandas.DataFrame
        """
        df = self._track_param(name=name)
        model = self._series_dict[name].unit("last").model
        cols = list(set(df.columns) & set(model.PARAMETERS))
        if params is not None:
            if not isinstance(params, (list, set)):
                raise TypeError(
                    f"@params must be a list of parameters, but {params} were applied.")
            cols = list(set(cols) & set(params)) or cols
        df = df.loc[:, cols] / df.loc[df.index[0], cols]
        if show_figure:
            f_date = df.index[0].strftime(self.DATE_FORMAT)
            title = f"{self.area}: {model.NAME} parameter change rates over time (1.0 on {f_date})"
            ylabel = f"Value per that on {f_date}"
            title = f"{self.area}: {ylabel} over time"
            tracker = self._create_tracker(self.MAIN)
            line_plot(
                df, title, ylabel=ylabel, v=tracker.change_dates(),
                math_scale=False, filename=filename)
        return df

    def retrospective(self, beginning_date, model, control="Main", target="Target", **kwargs):
        """
        Perform retrospective analysis.
        Compare the actual series of phases (control) and
        series of phases with specified parameters (target).

        Args:
            beginning_date (str): when the parameter values start to be changed from actual values
            model (covsirphy.ModelBase): ODE model
            control (str): scenario name of control
            target (str): scenario name of target
            kwargs: keyword argument of parameter values and Estimator.run()

        Notes:
            When parameter values are not specified,
            actual values of the last date before the beginning date will be used.
        """
        param_dict = {
            k: v for (k, v) in kwargs.items() if k in model.PARAMETERS}
        est_kwargs = dict(kwargs.items() - param_dict.items())
        # Control
        self.clear(name=control, include_past=True)
        self.trend(name=control, show_figure=False)
        tracker = self._create_tracker(control)
        try:
            tracker.separate(beginning_date)
        except ValueError:
            pass
        self.estimate(model, name=control, **est_kwargs)
        # Target
        self.clear(name=target, include_past=False, template=control)
        phases_changed = [
            self.num2str(i) for (i, ph) in enumerate(self._series_dict[target])
            if ph >= beginning_date
        ]
        self.delete(phases_changed, name=target)
        self.add(name=target, **param_dict)
        self.estimate(model, name=target, **est_kwargs)

    def score(self, metrics="RMSLE", variables=None, phases=None, past_days=None, name="Main", y0_dict=None):
        """
        Evaluate accuracy of phase setting and parameter estimation of all enabled phases all some past days.

        Args:
            metrics (str): "MAE", "MSE", "MSLE", "RMSE" or "RMSLE"
            variables (list[str] or None): variables to use in calculation
            phases (list[str] or None): phases to use in calculation
            past_days (int or None): how many past days to use in calculation, natural integer
            name(str): phase series name. If 'Main', main PhaseSeries will be used
            y0_dict(dict[str, float] or None): dictionary of initial values of variables

        Returns:
            float: score with the specified metrics

        Notes:
            If @variables is None, ["Infected", "Fatal", "Recovered"] will be used.
            "Confirmed", "Infected", "Fatal" and "Recovered" can be used in @variables.
            If @phases is None, all phases will be used.
            @phases and @past_days can not be specified at the same time.
        """
        name_temp = f"{name}_temporally_for_scoring"
        self.clear(name=name_temp, include_past=False, template=name)
        tracker = self._create_tracker(name_temp)
        if past_days is not None:
            if phases is not None:
                raise ValueError(
                    "@phases and @past_days cannot be specified at the same time.")
            past_days = self.ensure_natural_int(past_days, name="past_days")
            # Separate a phase, if possible
            beginning_date = self.date_change(
                self.last_date, days=0 - past_days)
            try:
                tracker.separate(date=beginning_date)
            except ValueError:
                pass
            # Ge the list of target phases
            phases = [
                self.num2str(num) for (num, unit)
                in enumerate(self._series_dict[name_temp])
                if unit >= beginning_date
            ]
        score = tracker.score(
            metrics=metrics, variables=variables, phases=phases, y0_dict=y0_dict)
        if name_temp != name:
            self.delete(name=name_temp)
        return score
