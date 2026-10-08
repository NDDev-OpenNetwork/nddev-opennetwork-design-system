import 'package:flutter/material.dart';

import 'tokens.dart';

abstract final class OpenNetworkTheme {
  static ThemeData dark() {
    final scheme = ColorScheme.fromSeed(
      seedColor: OpenNetworkColors.accentCyan,
      brightness: Brightness.dark,
      surface: OpenNetworkColors.surface800,
    );
    return ThemeData(
      brightness: Brightness.dark,
      colorScheme: scheme.copyWith(
        primary: OpenNetworkColors.accentCyan,
        secondary: OpenNetworkColors.accentViolet,
        surface: OpenNetworkColors.surface800,
        error: OpenNetworkColors.statusDanger,
      ),
      scaffoldBackgroundColor: OpenNetworkColors.space950,
      cardColor: OpenNetworkColors.surface800,
      useMaterial3: true,
      inputDecorationTheme: const InputDecorationTheme(
        border: OutlineInputBorder(),
      ),
      focusColor: OpenNetworkColors.focusRing,
    );
  }
}
