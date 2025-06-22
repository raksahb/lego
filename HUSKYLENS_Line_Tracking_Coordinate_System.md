# HUSKYLENS Line Tracking Coordinate System

## Overview
The HUSKYLENS AI vision sensor uses a specific coordinate system when identifying and tracking lines. This document outlines how the coordinate system works specifically for line tracking functionality.

## Display Specifications
- **Screen Resolution**: 320×240 pixels
- **Display Type**: 2.0-inch IPS screen
- **Coordinate Origin**: Top-left corner (0,0)

## Coordinate System Layout

### Basic Coordinate Structure
The HUSKYLENS uses a standard screen coordinate system where:
- **X-axis**: Runs horizontally from left to right (0 to 319)
- **Y-axis**: Runs vertically from top to bottom (0 to 239)
- **Origin Point**: Located at the top-left corner (0,0)

```
(0,0) ────────────────────────── (320,0)
  │                                 │
  │                                 │
  │                                 │
  │           Screen                │
  │                                 │
  │                                 │
  │                                 │
(0,240) ──────────────────────── (320,240)
```

## Line Tracking Specific Coordinates

### Arrow Representation
When the HUSKYLENS identifies a line, it represents the line as an **arrow** with the following coordinate data:

#### Arrow Coordinate Parameters:
- **xOrigin**: X-coordinate of the arrow's starting point
- **yOrigin**: Y-coordinate of the arrow's starting point  
- **xTarget**: X-coordinate of the arrow's ending point
- **yTarget**: Y-coordinate of the arrow's ending point
- **ID**: Identification number of the tracked line

### Data Format
```
Arrow: xOrigin=X1, yOrigin=Y1, xTarget=X2, yTarget=Y2, ID=LineID
```

## Line Direction and Prediction

### Arrow Direction Interpretation
The arrow indicates the **predicted direction** of the line:
- The arrow starts at (`xOrigin`, `yOrigin`)
- The arrow points toward (`xTarget`, `yTarget`)
- The direction from origin to target shows the line's predicted path

### Learning Position Requirements
When learning a line:
- Position the HUSKYLENS **parallel to the line** for optimal detection
- Ensure the line is clearly visible within the camera's field of view
- The "+" symbol in the center should be pointed at the line during learning

## Visual Indicators

### Color Coding During Operation
- **White Arrow**: Line detected but not yet learned
- **Blue Arrow**: Learned line recognized and being tracked
- **Yellow Frame**: Line currently being learned (during learning process)

### Frame States
1. **Detection Phase**: White arrow appears when line is detected
2. **Learning Phase**: Yellow frame with "Learning: ID1" text
3. **Recognition Phase**: Blue arrow with directional prediction

## Technical Considerations

### Line Requirements
- **Monochrome Lines**: Single color lines work best
- **High Contrast**: Line color should contrast clearly with background
- **Lighting Stability**: Consistent ambient lighting improves accuracy
- **Line Width**: Adequate width for reliable detection

### Coordinate Accuracy
- Coordinates are provided as integer pixel values
- Range: X (0-319), Y (0-239)
- Real-time updates as the line moves within the field of view

## Programming Interface

### Data Retrieval
When programming with Arduino or micro:bit, line tracking data is accessed through:
```
if (result.command == COMMAND_RETURN_ARROW) {
    int startX = result.xOrigin;
    int startY = result.yOrigin;
    int endX = result.xTarget;
    int endY = result.yTarget;
    int lineID = result.ID;
}
```

### Coordinate Conversion
To convert screen coordinates to real-world positioning:
1. Determine the physical field of view dimensions
2. Calculate the pixel-to-distance ratio
3. Apply trigonometric calculations for angle determination

## Practical Applications

### Robot Navigation
- Use arrow direction to determine steering commands
- Calculate deviation from center line using coordinate differences
- Implement PID control based on coordinate feedback

### Line Following Logic
1. Check if line is detected (arrow coordinates available)
2. Calculate line center position relative to screen center
3. Determine turning direction based on coordinate deviation
4. Adjust robot movement to follow the predicted line path

## Limitations and Best Practices

### Environmental Factors
- Ambient lighting affects line color detection
- Shadows and reflections can interfere with tracking
- Multiple crossing lines should be avoided during learning

### Optimal Setup
- Mount HUSKYLENS at consistent height above the line
- Ensure adequate lighting without shadows
- Test line tracking in actual operating environment
- Calibrate coordinate-to-movement ratios for specific robot platform

## Summary
The HUSKYLENS coordinate system for line tracking provides precise pixel-level positioning data through arrow coordinates, enabling accurate line following and path prediction for robotics applications. Understanding the coordinate system is essential for implementing effective line-following algorithms and robot navigation systems.
