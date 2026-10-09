import 'package:flutter/material.dart';

import 'tokens.dart';

abstract final class OpenNetworkTheme {
  static ThemeData dark() {
    final scheme =
        ColorScheme.fromSeed(
          seedColor: OpenNetworkColors.accentCyan,
          brightness: Brightness.dark,
          surface: OpenNetworkColors.surface800,
        ).copyWith(
          primary: OpenNetworkColors.accentCyan,
          onPrimary: OpenNetworkColors.space950,
          secondary: OpenNetworkColors.accentViolet,
          onSecondary: OpenNetworkColors.space950,
          surface: OpenNetworkColors.surface800,
          onSurface: OpenNetworkColors.text100,
          onSurfaceVariant: OpenNetworkColors.text300,
          error: OpenNetworkColors.statusDanger,
          onError: OpenNetworkColors.space950,
        );
    final base = ThemeData(
      colorScheme: scheme,
      scaffoldBackgroundColor: OpenNetworkColors.space950,
      cardColor: OpenNetworkColors.surface800,
      useMaterial3: true,
      // No font download or bundled font is required; the platform supplies
      // its native fallback when a preferred family is unavailable.
      fontFamily: OpenNetworkTypography.fontFamily.first,
      fontFamilyFallback: OpenNetworkTypography.fontFamily.skip(1).toList(),
      inputDecorationTheme: const InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.all(Radius.circular(OpenNetworkRadii.md)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.all(Radius.circular(OpenNetworkRadii.md)),
          borderSide: BorderSide(color: OpenNetworkColors.focusRing),
        ),
        contentPadding: EdgeInsets.all(OpenNetworkSpacing.four),
      ),
      focusColor: OpenNetworkColors.focusRing,
    );
    return base.copyWith(
      textTheme: base.textTheme.copyWith(
        bodyMedium: base.textTheme.bodyMedium?.copyWith(
          fontSize: OpenNetworkTypography.bodySize,
          height: OpenNetworkTypography.bodyLineHeight,
        ),
        headlineSmall: base.textTheme.headlineSmall?.copyWith(
          fontSize: OpenNetworkTypography.headingSize,
        ),
      ),
    );
  }
}
