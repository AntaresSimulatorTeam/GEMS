# Calendar

The **Calendar** is used by [View config](view-config.md) in order to date views by **Time Mapping** the simulation time with the real dates. .

## Key elements in calendar file

The calendar file is a csv file referenced by this terminology.

| Element | Type | Description |
|------|------|--------------------------|
| `calendar.id` | String | A unique identifier for the calendar.|
| `calendar.dataframe` | DataFrame | Calendar frame containing the reference between the views timeline and the real timeline.|

### Calendar DataFrame

The `calendar.dataframe` is structured following this configuration :

| Element | Type | Description |
|------|------|--------------------------|
| `absolute time index` | Date | Absolute time index used by the view.|
| `block` | String | Elements eferenced by the row.|
| `granular date` | Date | Real and Human-Readable date.|

## Example

This example presents a sample of `calendar`.

```csv
absolute_time_index	block	granular_date
0	1	2025-01-01 00:00:00
1	1	2025-01-01 01:00:00
2	1	2025-01-01 02:00:00
```