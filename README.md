# BL Crop Raid Report — User Guide

This guide walks you through configuring and running the Big Life Crop Raid Report workflow, which ingests human-wildlife conflict crop raid events from EarthRanger and produces a comprehensive incident analysis report for the Amboseli ecosystem.

---

## Overview

The workflow delivers, for each run:

- **Charts** — time-of-day incident distribution, damage size boxplot by ranger response timing, monthly incidents by crop raid location, crop species pie charts (by count and by area), monthly incidents and damage stacked bars
- **Maps** — crop raid density grid, timing of ranger response scatter map, species responsible scatter map, and a per-month crop destroyed scatter map (one view per month)
- **Summary tables** — elephant damage by month, mean elephant group size, ranger response timing with percentages, total acres damaged, species damage, crop damage (6 GeoParquet files)
- A **Word document report** (`overall_report.docx`) — all charts, maps, and tables assembled into the Big Life crop raid report template, downloaded automatically from Dropbox
- An **interactive dashboard** — 17 widgets covering every chart, map, and table produced by the run (the per-month crop maps are merged into a single switchable widget)

The three Amboseli geospatial layers and the Word report template are downloaded automatically from Dropbox at run time. No additional setup is required for these.

---

## Prerequisites

Before running the workflow, ensure you have:

- Access to an **EarthRanger** instance with `hwc_crop_raids` events logged for the analysis period

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In the workflow runner, go to **Workflow Templates** and click **Add Workflow Template**. Paste the GitHub repository URL into the **Github Link** field:

```
https://github.com/wildlife-dynamics/bl_crop_raid_report.git
```

Then click **Add Template**.

![Add Workflow Template](data/screenshots/add_workflow.png)

---

### Step 2 — Add an EarthRanger Connection

Navigate to **Data Sources** and click **Connect**. Select **EarthRanger** from the data source type dialog, then fill in the connection form:

- **Data Source Name** — a label to identify this connection
- **EarthRanger URL** — your instance URL (e.g. `your-site.pamdas.org`)
- **EarthRanger Username** and **EarthRanger Password**

> Credentials are not validated at setup time. Any authentication errors will appear when the workflow runs.

Click **Connect** to save.

![EarthRanger Connection](data/screenshots/er_connection.png)

---

### Step 3 — Select the Workflow

After the template is added, it appears in the **Workflow Templates** list as **bl_crop_raid_report**. Click it to open the workflow configuration form.

> The card may show **Initializing…** briefly while the environment is set up.

![Select Workflow Template](data/screenshots/select_workflow.png)

---

### Step 4 — Set Workflow Details, Report Time Range, and Connect to EarthRanger

The configuration form has three sections.

**Set Workflow Details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run |
| Workflow Description | Optional notes (e.g. month, site, or reporting period) |

**Set Report Time Range**

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start date and time of the analysis period |
| Until | End date and time of the analysis period |

All crop raid events are fetched within this window. Monthly breakdowns in the charts and maps are derived from the event timestamps within this range.

**Connect to EarthRanger**

Select the EarthRanger data source configured in Step 2 from the **Data Source** dropdown (e.g. `Amboseli Trust for Elephants`).

![Set Workflow Details, Report Time Range, and Connect to EarthRanger](data/screenshots/workflow_details_time_range_connection.png)

---

## Running the Workflow

Once all parameters are configured, click **Submit**. The runner will:

1. Download the Amboseli land-use, ranch boundary, and electric fence layers from Dropbox and reproject them to EPSG:4326.
2. Fetch `hwc_crop_raids` events from EarthRanger for the specified time range.
3. Process and normalise event details (field titles, numeric conversions, 3-hour time bins).
4. Generate all 7 charts and persist as HTML and PNG.
5. Generate the density grid map, timing-of-response map, species map, and a per-month crop-destroyed map (one view per month).
6. Compute 6 summary tables and persist as GeoParquet files.
7. Download the Big Life crop raid Word template from Dropbox and populate it with all charts, maps, and tables.
8. Assemble the 17-widget dashboard.
9. Save all files to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

---

## Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`:

| File | Description |
|------|-------------|
| `time_bin_bar_chart` (`.html` + `.png`) | Time of day bar chart (3-hour bins) |
| `damage_size_boxplot` (`.html` + `.png`) | Damage size boxplot by ranger response timing |
| `monthly_crop_raid_location_incidents` (`.html` + `.png`) | Monthly incidents stacked by crop raid location |
| `proportion_crop_species_targeted` (`.html` + `.png`) | Crop species pie chart by incident count (Core AOO, damage-confirmed incidents only) |
| `proportion_land_damaged` (`.html` + `.png`) | Crop species pie chart by total acres damaged (Core AOO, damage-confirmed incidents only) |
| `total_incidents_recorded` (`.html` + `.png`) | Monthly incidents stacked by crop (Core AOO; only the 6 named crops are broken out, all others grouped as "Other") |
| `total_damage_recorded` (`.html` + `.png`) | Monthly damage stacked by crop (Core AOO; see note below) |
| `crop_raid_incident_density_map` (`.html` + `.png`) | Density grid map of all crop raid incidents |
| `timing_of_response_event_map` (`.html` + `.png`) | Scatter map coloured by ranger response timing |
| `species_responsible_event_map` (`.html` + `.png`) | Scatter map coloured by species responsible |
| `<month>` (`.html` + `.png`, one per month) | Per-month crop-destroyed scatter map |
| `total_land_size_damaged_by_elephants` (GeoParquet) | Elephant damage by month and crop species (acres) |
| `average_elephant_group_size_over_time` (GeoParquet) | Mean elephant group size per month |
| `timing_of_ranger_response` (GeoParquet) | Ranger response timing crosstab with percentages |
| `total_area_damaged_by_crop_raid_location` (GeoParquet) | Acres damaged by response timing and location |
| `total_land_damage_by_species_responsible` (GeoParquet) | Species incidents and acres by crop raid location |
| `total_crops_damaged_by_species` (GeoParquet) | Crop incidents and acres by crop raid location |
| `overall_report.docx` | Final populated Word crop raid report |

> **Note:** despite its "Acres" axis label, `total_damage_recorded` is not currently filtered to acre-measured events — it charts `Damage size` across whatever measurement units are present. If your EarthRanger data mixes acres with other units, treat this chart as indicative rather than a strict acreage total; see [Troubleshooting](docs/troubleshooting.html).
