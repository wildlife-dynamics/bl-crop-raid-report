"""
Generate the BL Crop Raid Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: bl_crop_raid_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from datetime import date

OUTPUT_FILE = "bl_crop_raid_report_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
GREEN_LIGHT = colors.HexColor("#d8f3dc")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)

H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")

BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10,
                  bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)
def code(text):          return Paragraph(text, CODE)

def c(text):
    """Wrap text in a Paragraph for use inside Table cells."""
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


# ── Page template ──────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN_DARK)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 7, "BL Crop Raid Report — Technical Guide")
    canvas.drawRightString(w - 1.5*cm, 7, f"Page {doc.page}")
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.restoreState()


# ── Build story ────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="BL Crop Raid Report — Technical Guide",
        author="Ecoscope",
    )

    story = []

    # ── Cover ──────────────────────────────────────────────────────────────────
    story += [
        sp(60),
        p("BL Crop Raid Report", TITLE),
        p("Technical Guide", SUBTITLE),
        sp(8),
        hr(),
        p("Human-Wildlife Conflict Analysis — Methodology &amp; Calculation Reference", META),
        p(f"Version 2.0  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
        hr(),
        PageBreak(),
    ]

    # ── 1. Overview ───────────────────────────────────────────────────────────
    story += [
        h1("1. Overview"),
        hr(),
        p(
            "The <b>BL Crop Raid Report</b> workflow is a data-to-report pipeline "
            "built for Big Life Foundation's human-wildlife conflict (HWC) monitoring "
            "programme in the Amboseli ecosystem. It ingests crop raid events of type "
            "<code>hwc_crop_raids</code> from <b>EarthRanger</b>, transforms and "
            "classifies the event details, and produces charts, maps, summary tables, "
            "a Word report, and a dashboard."
        ),
        sp(4),
        note(
            "Version 2.0 rewrites this guide against the current <code>spec.yaml</code> "
            "(id <code>crop_raid_report</code>). It corrects the dependency list "
            "(migrated to <code>ecoscope-platform</code>), the real task names — "
            "several in the previous version (e.g. <code>generate_density_grid</code>, "
            "<code>draw_custom_stacked_bar_chart</code>, <code>zip_groupbykey</code>, "
            "<code>extract_dt_attributes</code>) matched nothing in <code>spec.yaml</code> — "
            "the Word report's fixed <code>\"Ecoscope\"</code> author field and "
            "<code>overall_report.docx</code> filename, and the dashboard, which wires "
            "up 17 widgets rather than an empty/metadata-only one."
        ),
        sp(4),
        p("The workflow delivers the following outputs per run:"),
        make_table(
            [
                ["Category",       "Outputs"],
                ["Charts",         "Time-of-day bar chart, damage size boxplot, monthly crop raid locations, crop species pie charts (count + area), monthly incidents and damage stacked bars — 7 charts total"],
                ["Maps",           "Crop raid density grid map, timing-of-ranger-response scatter map, species-responsible scatter map, and a per-month crop-destroyed scatter map (one view per month present in the data)"],
                ["Summary tables", "6 GeoParquet tables (+ matching HTML dashboard tables): elephant damage by month, mean elephant group size, ranger response timing, total acres damaged, species damage, crop damage"],
                ["Report",         "Word document (overall_report.docx): Big Life crop raid template populated with every chart, map, and table"],
                ["Dashboard",      "17 widgets — every chart, map, and table above (the per-month crop maps are merged into a single switchable widget)"],
            ],
            [4*cm, 12.5*cm],
        ),
    ]

    # ── 2. Dependencies ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("2. Dependencies &amp; Prerequisites"), hr(),

        h2("2.1 Python packages"),
        p("The workflow declares eight versioned packages, resolved from the Ecoscope prefix.dev channels:"),
        make_table(
            [
                ["Package",                            "Version",       "Channel"],
                ["ecoscope-platform",                   "2.18.0",        "ecoscope-workflows"],
                ["ecoscope-workflows-ext-custom",       "0.1.0rc14.*",   "ecoscope-workflows-custom"],
                ["ecoscope-workflows-ext-ste",          "0.0.0rc1.*",    "ecoscope-workflows-custom"],
                ["ecoscope-workflows-ext-mnc",          "1.0.0.*",       "ecoscope-workflows-custom"],
                ["ecoscope-workflows-ext-wwf-virunga",  "0.0.0rc9.*",    "ecoscope-workflows-custom"],
                ["ecoscope-workflows-ext-big-life",     "1.0.1.*",       "ecoscope-workflows-custom"],
                ["pydeck",                              "0.9.2",         "conda-forge"],
                ["opentelemetry-sdk",                   "&gt;=1.20.0,&lt;2.0.0", "conda-forge"],
            ],
            [6.5*cm, 3.2*cm, 6.3*cm],
        ),
        p(
            "The bar, pie, and boxplot chart tasks come from "
            "<code>ecoscope-workflows-ext-wwf-virunga</code>. Nearly all crop-raid-specific "
            "transformation tasks (time-bin assignment, crosstab summaries, row ordering, "
            "percentage strings, column suffixes, aggregation, boxplot rendering, and the "
            "Word report generator) come from <code>ecoscope-workflows-ext-big-life</code>. "
            "Integer conversion and missing-value filling come from "
            "<code>ecoscope-workflows-ext-mnc</code>. The Dropbox fetch, event-detail title "
            "mapping, geojson/scatterplot layer creation, and map-layer combination tasks "
            "come from <code>ecoscope-workflows-ext-ste</code> and "
            "<code>ecoscope-workflows-ext-custom</code>."
        ),

        sp(4), h2("2.2 EarthRanger Connection"),
        p(
            "All crop raid data is sourced from an <b>EarthRanger</b> instance via "
            "<code>set_er_connection</code>. The workflow fetches events of type "
            "<code>hwc_crop_raids</code> using <code>get_events</code>. "
            "<code>raise_on_empty: true</code> causes the workflow to halt with an "
            "error if no events are found — distinguishing a data-availability "
            "problem from a genuine zero-incident period. "
            "<code>include_display_values: true</code> ensures choice fields are "
            "returned as human-readable labels rather than internal codes."
        ),

        sp(4), h2("2.3 Static Geospatial Layers"),
        p(
            "Three GeoPackage files are downloaded from Dropbox at run time "
            "(<code>overwrite_existing: false</code>, 3 retries) and reprojected to "
            "<b>EPSG:4326</b> before use."
        ),
        make_table(
            [
                ["File",                                                   "Used for",                          "Key column"],
                ["amboseli_ranch_conservancies_layers.gpkg",               "Land-use fill polygons on all maps", "land_use (5 categories)"],
                ["amboseli_group_ranch_boundaries_x_electric_fence.gpkg",  "Ranch boundaries + electric fence",  "land_use (Ranch boundaries, Electric Fence)"],
                ["amboseli_group_ranch_boundaries.gpkg",                   "Downloaded and reprojected, not otherwise used downstream", "—"],
            ],
            [6*cm, 6*cm, 3.5*cm],
        ),

        sp(4), h2("2.4 Base Map Tile Layers"),
        make_table(
            [
                ["Layer",                  "URL (abbreviated)",                       "Opacity", "Max zoom"],
                ["ESRI World Hillshade",    "arcgisonline.com/…/World_Hillshade/…",    "1.0",     "20"],
                ["ESRI World Street Map",  "arcgisonline.com/…/World_Street_Map/…",   "0.15",    "20"],
            ],
            [4.5*cm, 7*cm, 2*cm, 2.5*cm],
        ),

        sp(4), h2("2.5 Land-use and Boundary Layer Styles"),
        p("Land-use polygons are coloured by <code>land_use</code> value (<code>apply_color_map</code> + <code>create_geojson_layer</code>, 75% opacity):"),
        make_table(
            [
                ["Category",                   "Hex colour"],
                ["Rangeland",                  "#a39c91"],
                ["Rangeland and settlement",   "#ffa07a"],
                ["Settlement and agriculture", "#2f4f4f"],
                ["Conservancies",              "#8fbc8b"],
                ["National parks and reserves","#4d6600"],
            ],
            [7*cm, 8.5*cm],
        ),
        p("Ranch boundaries and electric fence are separate line layers (no fill):"),
        make_table(
            [
                ["Feature",         "Colour",     "Width / Opacity"],
                ["Ranch boundaries","#000000  —  black",  "0.95 px / 55%"],
                ["Electric Fence",  "#2d62b1",             "5.5 px / 100%"],
            ],
            [4*cm, 6*cm, 5.5*cm],
        ),

        sp(4), h2("2.6 Grouping Strategy"),
        p(
            "The grouper is fixed to <code>ts_month_name</code> — the calendar month "
            "name derived from the event timestamp (<code>set_groupers</code>, not "
            "user-configurable). This drives the <code>split_by_month</code> fan-out "
            "that produces one crop-destroyed map per month present in the data."
        ),
    ]

    # ── 3. Event Data Pipeline ────────────────────────────────────────────────
    story += [
        sp(4), h1("3. Event Data Pipeline"), hr(),

        h2("3.1 Event Fetch — hwc_crop_raids"),
        p(
            "<code>get_events</code> queries EarthRanger for events of type "
            "<code>hwc_crop_raids</code>, with <code>include_details: true</code>, "
            "<code>include_display_values: true</code>, and "
            "<code>force_point_geometry: true</code>. Only events with a valid point "
            "geometry are included."
        ),
        p("Columns retrieved per event:"),
        bullet("id, time, event_type, event_category, reported_by, serial_number, geometry, created_at, event_details"),

        sp(4), h2("3.2 Event Details Processing"),
        p(
            "<code>process_events_details</code> (id <code>process_crop_details</code>) "
            "is called with <code>map_to_titles: true</code> and <code>ordered: true</code>, "
            "mapping each field's internal key to its EarthRanger display title (e.g. "
            "&ldquo;Main crop destroyed&rdquo;, &ldquo;Crop raid location&rdquo;, "
            "&ldquo;Species responsible&rdquo;) and preserving field order."
        ),

        sp(4), h2("3.3 JSON Normalisation and Prefix Removal"),
        p(
            "<code>normalize_json_column</code> flattens <code>event_details</code> "
            "into individual <code>event_details__&lt;title&gt;</code> columns. "
            "<code>drop_column_prefix</code> then strips the <code>event_details__</code> "
            "prefix (<code>duplicate_strategy: keep_original</code>)."
        ),

        sp(4), h2("3.4 Column Selection and Type Conversion"),
        p(
            "<code>map_columns</code> drops four administrative columns not used in "
            "analysis: <code>event_category</code>, <code>event_type</code>, "
            "<code>reported_by</code>, <code>event_type_display</code>. All other "
            "detail fields are retained as-is."
        ),
        p("Two numeric conversions follow:"),
        bullet("<b>Damage size → float</b> (<code>ecoscope_workflows_ext_big_life.tasks.transformation.convert_columns_to_float</code>, errors coerced, null filled with 0)"),
        bullet("<b>Number of animals → int</b> (<code>ecoscope_workflows_ext_mnc.tasks.transformation.convert_columns_to_int</code>, errors coerced, null filled with 0)"),
        p(
            "<code>fill_missing_values</code> then fills blanks in <b>Time of ranger "
            "response</b>, <b>Species responsible</b>, and <b>Main crop destroyed</b> "
            "with the string <code>\"Unknown\"</code>."
        ),

        sp(4), h2("3.5 Temporal Attribute Extraction"),
        p(
            "<code>decompose_datetime</code> (id <code>extract_date</code>) derives "
            "three columns from <b>Date and time of raid</b>, all prefixed <code>ts_</code>:"
        ),
        make_table(
            [
                ["Derived column",   "Attribute", "Example value"],
                ["ts_month",         "month",     "1 – 12 (integer)"],
                ["ts_month_name",    "month_name","January, February, …"],
                ["ts_hour",          "hour",      "0 – 23 (integer)"],
            ],
            [4*cm, 3*cm, 9.5*cm],
        ),

        sp(4), h2("3.6 Time Bin Assignment"),
        p(
            "<code>assign_time_bins</code> (from <code>ecoscope-workflows-ext-big-life</code>) "
            "groups <code>ts_hour</code> into 3-hour bins, producing the "
            "<code>time_bin</code> column. Note the bins are labelled/ordered starting "
            "at midday, not midnight:"
        ),
        make_table(
            [
                ["Bin label",     "Hours covered"],
                ["12:01 – 15:00","12:01 to 15:00"],
                ["15:01 – 18:00","15:01 to 18:00"],
                ["18:01 – 21:00","18:01 to 21:00"],
                ["21:01 – 00:00","21:01 to midnight"],
                ["00:00 – 03:00","Midnight to 03:00"],
                ["03:01 – 06:00","03:01 to 06:00"],
                ["06:01 – 09:00","06:01 to 09:00"],
                ["09:01 – 12:00","09:01 to 12:00"],
            ],
            [5*cm, 11.5*cm],
        ),
        p(
            "All subsequent charts, maps, and tables operate on this enriched "
            "DataFrame (<code>assign_custom_bins.return</code>)."
        ),
    ]

    # ── 4. Chart Outputs ──────────────────────────────────────────────────────
    story += [
        sp(4), h1("4. Chart Outputs"), hr(),

        h2("4.1 Time of Day Bar Chart"),
        p(
            "<code>ecoscope_workflows_ext_big_life.tasks.transformation.aggregate_by</code> "
            "counts events per <code>time_bin</code>; <code>draw_bar_chart</code> "
            "(grouped mode) then renders the distribution across the fixed "
            "12:01&rarr;09:00 bin order (see &sect;3.6). Bar colour "
            "<code>#6495ed</code>; plot background <code>#f5f5f5</code>; legend hidden."
        ),
        p("Output: <b>time_bin_bar_chart</b>"),

        sp(4), h2("4.2 Damage Size Boxplot"),
        p(
            "<code>ecoscope_workflows_ext_big_life.tasks.results.draw_boxplot</code> "
            "shows the distribution of <b>Damage size</b> broken down by <b>Time of "
            "ranger response</b> (Before / During / After crop raid), restricted to "
            "rows where <b>Measurement unit == \"Acre\"</b>. Vertical orientation, "
            "points hidden, box colour <code>#7eb0d5</code>."
        ),
        p("Output: <b>damage_size_boxplot</b>"),

        sp(4), h2("4.3 Monthly Crop Raid Locations Stacked Bar"),
        p(
            "<code>draw_bar_chart</code> (stacked mode) counts incidents per month "
            "(<code>ts_month_name</code> category, <code>ts_month</code> counted), "
            "stacked by <b>Crop raid location</b>. Uses the full dataset — not "
            "restricted to Core AOO. Month order fixed January&rarr;December."
        ),
        make_table(
            [
                ["Crop raid location", "Colour"],
                ["Core AOO",           "#a6cee3"],
                ["Non-core AOO",       "#b2df8a"],
                ["Outside AOO",        "#fdbf6f"],
                ["Unknown",            "#cfcfc4"],
            ],
            [5*cm, 11.5*cm],
        ),
        p("Output: <b>monthly_crop_raid_location_incidents</b>"),

        sp(4), h2("4.4 Crop Species Pie Chart (Incident Count)"),
        p(
            "Filtered to <b>Core AOO</b> events where <b>Damage caused = \"Yes\"</b>. "
            "<code>aggregate_by</code> counts incidents per <b>Main crop destroyed</b>, "
            "then <code>draw_pie_chart</code> (<code>textinfo: percent</code>) renders "
            "the split. Each of 25 crop values (23 named crops + None + Unknown) has "
            "its own pastel colour."
        ),
        p("Output: <b>proportion_crop_species_targeted</b>"),

        sp(4), h2("4.5 Crop Damage Pie Chart (Area)"),
        p(
            "Same Core AOO / Damage-caused-Yes filter as &sect;4.4, further restricted "
            "to <b>Measurement unit == \"Acre\"</b>. Sums <b>Damage size</b> per crop "
            "species rather than counting incidents, so it shows proportion of land "
            "area destroyed, not incident frequency."
        ),
        p("Output: <b>proportion_land_damaged</b>"),

        sp(4), h2("4.6 Monthly Incidents Stacked Bar (Core AOO, Top Crops)"),
        p(
            "Filtered to <b>Core AOO</b> (all incidents, not restricted to "
            "damage-confirmed). <code>map_column_value</code> consolidates the 25 crop "
            "values into 6 named crops plus <i>Other</i> (<code>other_crops_destroyed</code>):"
        ),
        make_table(
            [
                ["Grouped value",  "Included"],
                ["Beans",          "Beans"],
                ["Maize",          "Maize"],
                ["Onion",          "Onion"],
                ["Tomatoes",       "Tomatoes"],
                ["Watermelon",     "Watermelon"],
                ["Other",          "All remaining crop values, including French beans, None, and Unknown"],
            ],
            [3.5*cm, 12*cm],
        ),
        note(
            "&ldquo;French beans&rdquo; has its own colour swatch in the underlying "
            "colour map, but it is not one of the 6 explicit values in this chart's "
            "<code>stack_order</code>, and the grouping step maps it to <i>Other</i> "
            "rather than its own bucket — a mismatch worth being aware of if you see "
            "French beans incidents folded into the &ldquo;Other&rdquo; segment."
        ),
        p(
            "<code>draw_bar_chart</code> (stacked) plots monthly incident counts "
            "(y = count of <code>ts_month</code>) stacked by the grouped crop. Month "
            "order fixed January&rarr;December."
        ),
        p("Output: <b>total_incidents_recorded</b>"),

        sp(4), h2("4.7 Total Damage Stacked Bar"),
        p(
            "Same Core AOO filter and grouped-crop consolidation as &sect;4.6, with the "
            "y-axis set to <b>Damage size</b> (labelled &ldquo;Acres&rdquo;) instead of "
            "an incident count."
        ),
        note(
            "Unlike the boxplot (&sect;4.2) and the crop-damage pie chart (&sect;4.5), this "
            "chart's data source (<code>other_crops_rgba</code>) is <b>not</b> filtered "
            "to <code>Measurement unit == \"Acre\"</code> — a <code>filter_acre_aoo</code> "
            "task exists in <code>spec.yaml</code> for this purpose but its output is "
            "never referenced downstream. If your EarthRanger data records damage in "
            "mixed units, this chart's &ldquo;Acres&rdquo;-labelled axis may include "
            "non-acre values."
        ),
        p("Output: <b>total_damage_recorded</b>"),
    ]

    # ── 5. Map Outputs ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("5. Map Outputs"), hr(),
        p(
            "All maps share the same base-tile stack (Hillshade + Street Map) and "
            "the same land-use / boundary / fence static layers described in &sect;2.5, "
            "framed by a shared view state (<code>envelope_gdf</code>, expansion 1.05; "
            "<code>compute_view_state_from_gdf</code>, pitch 0, bearing 0, max zoom 15)."
        ),

        h2("5.1 Crop Raid Incident Density Map"),
        p(
            "<code>create_meshgrid</code> tessellates the full event extent with a "
            "2000 m grid (EPSG:3857); <code>calculate_feature_density</code> counts "
            "point events per cell. Zero-density cells are dropped, then "
            "<code>bin_column</code> classifies the remaining density values into 5 "
            "fixed bins (not data-driven quantiles, so density maps stay comparable "
            "across reporting periods):"
        ),
        make_table(
            [
                ["Bin",  "Count range", "Hex colour"],
                ["1",    "1 – 3",       "#FFF7BC"],
                ["2",    "4 – 6",       "#FD8D3C"],
                ["3",    "7 – 9",       "#F03B20"],
                ["4",    "10 – 12",     "#BD0026"],
                ["5",    "13+",         "#99000D"],
            ],
            [1.5*cm, 3*cm, 12*cm],
        ),
        p("Output: <b>crop_raid_incident_density_map</b>"),

        sp(4), h2("5.2 Timing of Ranger Response Map"),
        p("A scatter map (<code>create_scatterplot_layer</code>) coloured by <b>Time of ranger response</b>:"),
        make_table(
            [
                ["Response timing",  "Hex colour"],
                ["Before crop raid", "#a6cee3"],
                ["During crop raid", "#ff0000"],
                ["After crop raid",  "#d5b60a"],
                ["Unknown",          "#cfcfc4"],
            ],
            [5*cm, 11.5*cm],
        ),
        p("Radius 4 px, 75% opacity, black outline. Output: <b>timing_of_response_event_map</b>"),

        sp(4), h2("5.3 Species Responsible Map"),
        p("A scatter map coloured by <b>Species responsible</b>:"),
        make_table(
            [
                ["Species",  "Hex colour"],
                ["Baboon",   "#b3e2cd"],
                ["Buffalo",  "#fdcdac"],
                ["Eland",    "#cbd5e8"],
                ["Elephant", "#f4cae4"],
                ["Gazelle",  "#e6f5c9"],
                ["Giraffe",  "#fff2ae"],
                ["Impala",   "#f1e2cc"],
                ["Zebra",    "#cccccc"],
                ["Unknown",  "#cfcfc4"],
            ],
            [5*cm, 11.5*cm],
        ),
        p("Same styling as &sect;5.2. Output: <b>species_responsible_event_map</b>"),

        sp(4), h2("5.4 Per-Month Crop-Destroyed Maps (mapvalues fan-out)"),
        p(
            "One map is produced per calendar month present in the data, coloured by "
            "<b>Main crop destroyed</b> using the same 25-value colour palette as "
            "&sect;4.4. <code>split_by_month</code> (<code>split_groups</code> on "
            "<code>ts_month_name</code>) partitions the enriched event DataFrame; the "
            "colour assignment, scatterplot layer, layer combination, and view-state "
            "computation are each re-run per month via <code>mapvalues</code>/<code>map</code>. "
            "<code>column_first_unique_value</code> extracts the month name per "
            "partition, and <code>groupbykey</code> zips it onto the rendered map so "
            "each output file is suffixed with the correct month."
        ),
        p("Outputs: <b>&lt;month&gt;</b> (one file per month, e.g. <code>January</code>, <code>February</code>, …)"),
    ]

    # ── 6. Summary Tables ─────────────────────────────────────────────────────
    story += [
        sp(4), h1("6. Summary Tables"), hr(),
        p(
            "Six summary tables are persisted as GeoParquet, and each also gets a "
            "matching HTML render (<code>draw_table</code>, sortable/filterable, "
            "download enabled) for its dashboard table widget. All are built with "
            "<code>ecoscope_workflows_ext_big_life.tasks.transformation.crosstab_summary</code> "
            "or <code>aggregate_by</code>."
        ),
        make_table(
            [
                ["Output file",                             "Dimensions",                                    "Scope"],
                ["total_land_size_damaged_by_elephants",    "ts_month_name × Main crop destroyed, sum of Damage size", "Species responsible == Elephant, Measurement unit == Acre; rows ordered Jan→Dec"],
                ["average_elephant_group_size_over_time",  "ts_month_name → mean Number of animals",        "Same elephant + Acre filter; rows ordered Jan→Dec"],
                ["timing_of_ranger_response",              "Time of ranger response × Crop raid location, count + % strings", "All events; rows ordered Before→During→After"],
                ["total_area_damaged_by_crop_raid_location","Time of ranger response × Crop raid location, sum of Damage size + % strings", "Measurement unit == Acre only; same row order"],
                ["total_land_damage_by_species_responsible","Species responsible × Crop raid location, incidents + acres (merged)", "Incidents: all events; acres: Measurement unit == Acre only"],
                ["total_crops_damaged_by_species",          "Main crop destroyed × Crop raid location, incidents + acres (merged)", "Same incidents/acres split as above, indexed by crop"],
            ],
            [5.5*cm, 5.5*cm, 5*cm],
        ),
        note(
            "Percentage strings are added by <code>add_pct_str</code>, which computes "
            "each row's share of the total column and appends it in parentheses (e.g. "
            "<code>12 (42.9%)</code>), excluding the Total row/column from its own "
            "percentage calculation."
        ),
    ]

    # ── 7. Word Report &amp; Dashboard ────────────────────────────────────────
    story += [
        sp(4), h1("7. Word Report &amp; Dashboard"), hr(),

        h2("7.1 Template Download"),
        p(
            "The report template (<code>crop_raid_report_template.docx</code>) is "
            "downloaded automatically from Dropbox at run time "
            "(<code>fetch_and_persist_file</code>, up to 3 retries, "
            "<code>overwrite_existing: false</code>)."
        ),

        h2("7.2 Report Generation"),
        p("<code>generate_crop_raid_report</code> populates the template with every chart, map, and table:"),
        make_table(
            [
                ["Parameter",    "Value"],
                ["template_path","downloaded crop_raid_report_template.docx"],
                ["output_dir",   "$ECOSCOPE_WORKFLOWS_RESULTS"],
                ["filename",     "overall_report.docx"],
                ["time_period",  "the workflow's current time range"],
                ["generated_by", "\"Ecoscope\" (fixed string — not resolved from the EarthRanger user)"],
            ],
            [3.5*cm, 12*cm],
        ),
        p(
            "Chart screenshots use a 1 ms wait (self-contained HTML, batched across "
            "7 charts at 1280&times;720). Map screenshots use 40 000 ms to allow tile "
            "layers to load fully before capture."
        ),

        sp(4), h2("7.3 Dashboard"),
        p(
            "<code>gather_dashboard</code> registers <b>17 widgets</b> covering every "
            "chart, map, and table: 4 map widgets (density, response timing, species, "
            "and the per-month crop map — the last a merged multi-view widget built "
            "with <code>merge_widget_views</code>), 7 chart widgets, and 6 table widgets."
        ),
    ]

    # ── 8. Output Files ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("8. Output Files"), hr(),
        p("All outputs are written to <code>$ECOSCOPE_WORKFLOWS_RESULTS</code>."),
        make_table(
            [
                ["File",                                             "Format",     "Content"],
                ["time_bin_bar_chart",                                "HTML + PNG", "Time-of-day bar chart (3-hour bins)"],
                ["damage_size_boxplot",                               "HTML + PNG", "Damage size boxplot by ranger response timing"],
                ["monthly_crop_raid_location_incidents",              "HTML + PNG", "Monthly incident count stacked by crop raid location"],
                ["proportion_crop_species_targeted",                  "HTML + PNG", "Pie — crop species by incident count (Core AOO, damage-confirmed)"],
                ["proportion_land_damaged",                           "HTML + PNG", "Pie — crop species by acres damaged (Core AOO, damage-confirmed)"],
                ["total_incidents_recorded",                          "HTML + PNG", "Monthly incidents stacked by grouped crop (Core AOO)"],
                ["total_damage_recorded",                             "HTML + PNG", "Monthly damage stacked by grouped crop (Core AOO; see &sect;4.7 note)"],
                ["crop_raid_incident_density_map",                    "HTML + PNG", "Density grid of all crop raid events"],
                ["timing_of_response_event_map",                      "HTML + PNG", "Scatter map coloured by ranger response timing"],
                ["species_responsible_event_map",                     "HTML + PNG", "Scatter map coloured by species responsible"],
                ["&lt;month&gt; (one per month)",                     "HTML + PNG", "Per-month crop-destroyed scatter map"],
                ["total_land_size_damaged_by_elephants",              "GeoParquet + HTML", "Elephant damage by month × crop (acres)"],
                ["average_elephant_group_size_over_time",             "GeoParquet + HTML", "Mean elephant group size per month"],
                ["timing_of_ranger_response",                         "GeoParquet + HTML", "Ranger response timing crosstab with % strings"],
                ["total_area_damaged_by_crop_raid_location",          "GeoParquet + HTML", "Acres damaged by response timing × location"],
                ["total_land_damage_by_species_responsible",          "GeoParquet + HTML", "Species incidents + acres by crop raid location"],
                ["total_crops_damaged_by_species",                    "GeoParquet + HTML", "Crop incidents + acres by crop raid location"],
                ["overall_report.docx",                               "Word",       "Final populated crop raid report"],
            ],
            [6.5*cm, 3*cm, 7*cm],
        ),
    ]

    # ── 9. Workflow Execution Logic ───────────────────────────────────────────
    story += [
        sp(4), h1("9. Workflow Execution Logic"), hr(),

        h2("9.1 Skip Conditions"),
        p(
            "Every task carries the two default skip conditions via "
            "<code>task-instance-defaults</code>: <b>any_is_empty_df</b> and "
            "<b>any_dependency_skipped</b>. The event fetch, map-drawing, and "
            "scatterplot-layer tasks additionally carry explicit "
            "<code>skipif</code> blocks with both conditions."
        ),
        p(
            "The event fetch sets <code>raise_on_empty: true</code>, so a zero-event "
            "period surfaces as an explicit error rather than an empty, silently "
            "successful run."
        ),

        h2("9.2 mapvalues Fan-out (Per-Month Crop Maps)"),
        p(
            "<code>split_by_month</code> (<code>split_groups</code>) partitions the "
            "enriched event DataFrame by <code>ts_month_name</code>. Each task in the "
            "per-month pipeline (colour assignment, scatterplot layer, layer "
            "combination, view-state, map draw, persist, PNG conversion) re-runs once "
            "per month via <code>mapvalues</code>/<code>map</code>, and "
            "<code>groupbykey</code> zips the month name onto each rendered map before "
            "persisting, so output filenames are suffixed correctly."
        ),

        h2("9.3 Screenshot Timing"),
        make_table(
            [
                ["Task(s)",                       "wait_for_timeout", "Notes"],
                ["convert_chart_html_png (7 charts, batched)", "1 ms",  "1280&times;720; static Plotly HTML renders essentially instantly"],
                ["convert_density_map_png / convert_response_map_png / convert_species_map_png / convert_crop_map_png (×N months)", "40 000 ms", "Maps require full basemap tile rendering before capture"],
            ],
            [7*cm, 3*cm, 6.5*cm],
        ),

        h2("9.4 Core AOO Analysis Scope"),
        p(
            "Several charts (&sect;4.4&ndash;4.7) are scoped to <b>Core AOO</b> events only "
            "(<code>filter_row_values: column=\"Crop raid location\", values=[\"Core AOO\"]</code>), "
            "reflecting the operational focus on incidents within Big Life's core area "
            "of operation. The summary tables in &sect;6 and the location/species/timing "
            "charts in &sect;4.1&ndash;4.3 use the full dataset across all three location "
            "categories."
        ),
    ]

    # ── 10. Software Versions ─────────────────────────────────────────────────
    story += [
        sp(4), h1("10. Software Versions"), hr(),
        make_table(
            [
                ["Package",                          "Version",           "Channel"],
                ["ecoscope-platform",                 "2.18.0",            "ecoscope-workflows"],
                ["ecoscope-workflows-ext-custom",     "0.1.0rc14.*",       "ecoscope-workflows-custom"],
                ["ecoscope-workflows-ext-ste",        "0.0.0rc1.*",        "ecoscope-workflows-custom"],
                ["ecoscope-workflows-ext-mnc",        "1.0.0.*",           "ecoscope-workflows-custom"],
                ["ecoscope-workflows-ext-wwf-virunga","0.0.0rc9.*",        "ecoscope-workflows-custom"],
                ["ecoscope-workflows-ext-big-life",   "1.0.1.*",           "ecoscope-workflows-custom"],
                ["pydeck",                             "0.9.2",             "conda-forge"],
                ["opentelemetry-sdk",                  "&gt;=1.20.0,&lt;2.0.0", "conda-forge"],
            ],
            [6.5*cm, 4*cm, 6*cm],
        ),
        p(
            "Packages are distributed via the <code>prefix.dev</code> conda channels "
            "and pinned to patch/prerelease-compatible versions (<code>.*</code> "
            "suffix). The runtime environment is managed by <b>pixi</b>."
        ),
    ]

    # ── Build PDF ──────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
