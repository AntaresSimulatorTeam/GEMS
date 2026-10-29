# Calendar File

The **Calendar file** is used by the [View Configuration file](view-config.md) to date the [Views](../outputs/views.md): each time step of the [simulation table](../outputs/simulation-table.md) is dated thanks to the calendar.

## Location and naming

The calendar is a CSV file stored in the input folder of the study, next to the other input files (for example `input/calendar_file.csv`).

Its name, without the `.csv` extension, is given by `scope.calendar` in the [View Configuration file](view-config.md#scope). For example, `scope.calendar: calendar_file` refers to `calendar_file.csv`. This name is informative only: the calendar actually used is the calendar file provided as input.

## Format

The Calendar file is a CSV file with this configuration :

| Column | Type | Description |
| `absolute_time_index` | Integer | Time index from the [simulation table](../outputs/simulation-table.md). |
| `block` | Integer | It must match the `block` column of the simulation table. |
| `granular_date` | Datetime | Real date of the time step, written `YYYY-MM-DD HH:MM:SS` (like `2025-01-01 00:00:00`). The time step between two consecutive rows must be constant. Dates with a UTC offset (like `2025-01-01 00:00:00+01:00`) are converted to UTC, and periods (days, months, years) are then cut in UTC. |

### Example

This example presents a sample of `calendar` with hourly values beginning at the Jan. 1st 2026:

```csv
absolute_time_index,block,granular_date
0,0,2026-01-01 00:00:00
1,0,2026-01-01 01:00:00
2,0,2026-01-01 02:00:00
3,0,2026-01-01 03:00:00
```