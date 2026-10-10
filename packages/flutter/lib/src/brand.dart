import 'dart:math' as math;

import 'package:flutter/material.dart';

import 'brand_geometry.dart';
import 'tokens.dart';

/// The platform's authentic mark and stacked direction lockup.
class OpenNetworkBrand extends StatelessWidget {
  const OpenNetworkBrand({super.key});

  static double heightOf(BuildContext context) {
    final scale = MediaQuery.textScalerOf(context);
    return math.max(
      OpenNetworkSizes.brand,
      scale.scale(OpenNetworkTypography.bodyMin) *
              OpenNetworkTypography.bodyLeading +
          scale.scale(OpenNetworkTypography.captionMin) *
              OpenNetworkTypography.captionLeading,
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Semantics(
      label: 'NDDev OpenNetwork',
      child: ExcludeSemantics(
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            SizedBox.square(
              dimension: OpenNetworkSizes.brand,
              child: CustomPaint(painter: _Mark(theme.colorScheme.primary)),
            ),
            const SizedBox(width: OpenNetworkSpacing.three),
            Flexible(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'NDDev',
                    style: theme.textTheme.bodyMedium?.copyWith(
                      fontSize: OpenNetworkTypography.bodyMin,
                    ),
                  ),
                  Text(
                    'OpenNetwork',
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: theme.colorScheme.primary,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _Mark extends CustomPainter {
  _Mark(this.color);
  final Color color;
  @override
  void paint(Canvas canvas, Size size) {
    final scale = math.min(
      size.width / nddevMarkSize.width,
      size.height / nddevMarkSize.height,
    );
    canvas.save();
    canvas.translate(
      (size.width - nddevMarkSize.width * scale) / 2,
      (size.height - nddevMarkSize.height * scale) / 2,
    );
    canvas.scale(scale);
    canvas.drawPath(nddevMarkPath(), Paint()..color = color);
    canvas.restore();
  }

  @override
  bool shouldRepaint(_Mark oldDelegate) => color != oldDelegate.color;
}
