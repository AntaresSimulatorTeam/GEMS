# Calendar File

The **Calendar file** gives a real date to each time step of the [simulation table](../outputs/simulation-table.md). These dates are used to date the [Views](../outputs/views.md) and to aggregate their values over time, at the [`time-granularity`](view-config.md#aggregation-patterns) of each aggregation pattern (hour, day, week, month or year).

???+ info "Use by GEMS ViewsBuilder"
    The Calendar file is read by [GEMS ViewsBuilder](https://github.com/AntaresSimulatorTeam/GEMS-ViewsBuilder) (GVB), the tool that builds the Views from the simulation tables. It is given on the command line with the `--calendar` option, for example `--calendar study/calendar.csv`:

    - the file name is free, but its extension must be `.csv`;
    - a single Calendar file is used per run, for all the [View Configuration files](view-config.md) of the run;
    - the View Configuration file does not reference the calendar (`scope.calendar` was removed in GVB v0.1.0).

## Columns

The Calendar file is a CSV file with a comma separator and a header row. It has exactly the three columns below, in any order: a missing or extra column is rejected.

| Column | Type | Description |
|--------|------|-------------|
| `absolute_time_index` | Integer | Index of the time step, as in the `absolute_time_index` column of the [simulation table](../outputs/simulation-table.md). |
| `block` | Integer | Time block of the time step, as in the `block` column of the simulation table (`0` for a simulation run in a single block). |
| `granular_date` | Datetime | Real date of the time step, written `YYYY-MM-DD HH:MM:SS` (e.g. `2026-01-01 00:00:00`). A date with a UTC offset (e.g. `2026-01-01 00:00:00+01:00`) is converted to UTC, and the periods of the Views (days, weeks, months, years) are then cut in UTC. |

???+ warning "Write dates as `YYYY-MM-DD HH:MM:SS`"
    Dates in another format may be misread or not recognized. A date that is not recognized makes the building of the Views fail with the error ``InvalidOperationError: sub operation not supported for dtypes `str` and `str` ``, which does not mention the calendar.

## Rows

Each row gives the date of one time step. GVB checks two rules when it loads the calendar:

- `absolute_time_index` takes the values `0, 1, ..., N-1` in this order, without gaps: the first row has the index `0`, and each next row has the index of the previous row plus `1`;
- the step between the `granular_date` values of two consecutive rows is constant (for example one hour).

### Matching with the simulation table

Each row of the calendar dates the rows of the simulation table that have the same `absolute_time_index` **and** the same `block`:

- a time-dependent row of the simulation table is used in the Views only if its (`absolute_time_index`, `block`) pair is in the calendar. The time steps that are not in the calendar, such as those after its last row, are left out;
- the rows of outputs that do not depend on time (empty `absolute_time_index`) are always used, without a date.

The calendar can therefore cover only part of the simulation. A period of the Views that is only partly covered by the calendar is aggregated over its covered time steps only (see [Rows of a View](../outputs/views.md#rows-of-a-view)).

???+ warning "Calendar and simulation table must match"
    If no row of the calendar matches the simulation table (for example because of different `block` values), the Views are still produced without error, but each metric on time-dependent outputs only has a single row per location and breakdown value, with an empty `view_date` and `scenario_id` and a `0` value. Metrics on outputs that are not time-dependent keep their values, so the View can look partly correct.

## Example

This calendar dates an hourly simulation run in a single block and starting on 1 January 2026 at midnight (first rows only):

```csv
absolute_time_index,block,granular_date
0,0,2026-01-01 00:00:00
1,0,2026-01-01 01:00:00
2,0,2026-01-01 02:00:00
3,0,2026-01-01 03:00:00
```

With this calendar, the time step `absolute_time_index = 2` of block `0` of the simulation table is dated `2026-01-01 02:00:00`.
