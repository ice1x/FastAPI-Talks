# Image Assets for README

This directory contains visual assets for the README and documentation.

## Required Images

To complete the README visuals, please add the following images:

### 1. benchmark_comparison.png
- **Description**: Bar chart or line graph showing performance comparison of all 6 protocols
- **Dimensions**: 1200x600px (recommended)
- **How to generate**:
  ```bash
  python run_benchmarks.py
  python compare.py  # This generates benchmark_comparison.png
  mv benchmark_comparison.png docs/images/
  ```

### 2. dashboard_overview.png
- **Description**: Screenshot of the main dashboard page showing:
  - Statistics cards (total runs, protocols, metrics)
  - Comparison charts
  - Runs table
- **Dimensions**: 1400x900px (recommended)
- **How to generate**:
  ```bash
  python metrics_cli.py dashboard
  # Open http://localhost:8888 in browser
  # Take screenshot (full page if possible)
  ```

### 3. dashboard_detail.png (optional)
- **Description**: Screenshot of detailed run view showing:
  - Individual run statistics
  - Latency over time chart
  - Request metrics table
- **Dimensions**: 1400x900px (recommended)

## Placeholder Images

Until real images are added, the README references these paths but will show broken image icons. This is acceptable for initial commit.

## Image Optimization

Before committing, optimize images:

```bash
# Using ImageMagick
convert benchmark_comparison.png -resize 1200x600 -quality 85 benchmark_comparison.png

# Or using pngquant for better compression
pngquant --quality=80-95 dashboard_overview.png --output dashboard_overview.png
```

## Alternative: Use Badges Instead

If you prefer not to include large images initially, you can use only badges and text-based results tables, which are already included in the README.
