import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:nddev_opennetwork_design_system/opennetwork_design_system.dart';

void main() {
  test('theme uses canonical typography, radii and focus colors', () {
    final theme = OpenNetworkTheme.dark();
    expect(theme.brightness, Brightness.dark);
    expect(
      theme.textTheme.bodyMedium?.fontSize,
      OpenNetworkTypography.bodySize,
    );
    expect(
      theme.textTheme.bodyMedium?.height,
      OpenNetworkTypography.bodyLineHeight,
    );
    expect(
      theme.textTheme.headlineSmall?.fontSize,
      OpenNetworkTypography.headingSize,
    );
    final border =
        theme.inputDecorationTheme.focusedBorder! as OutlineInputBorder;
    expect(border.borderSide.color, OpenNetworkColors.focusRing);
    expect(border.borderRadius.topLeft.x, OpenNetworkRadii.md);
  });

  test('normal text and status foregrounds meet WCAG AA contrast', () {
    final colors = OpenNetworkTheme.dark().colorScheme;
    for (final pair in [
      (colors.primary, colors.onPrimary),
      (colors.secondary, colors.onSecondary),
      (colors.surface, colors.onSurface),
      (colors.surface, colors.onSurfaceVariant),
      (colors.error, colors.onError),
      (OpenNetworkColors.surface800, OpenNetworkColors.text500),
    ]) {
      expect(contrast(pair.$1, pair.$2), greaterThanOrEqualTo(4.5));
    }
    expect(
      contrast(OpenNetworkColors.focusRing, colors.surface),
      greaterThanOrEqualTo(3),
    );
  });

  testWidgets('native widgets render English and Russian at 200% text scale', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(360, 800);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    await tester.pumpWidget(
      MaterialApp(
        theme: OpenNetworkTheme.dark(),
        builder: (context, child) => MediaQuery(
          data: MediaQuery.of(context)
              .copyWith(textScaler: const TextScaler.linear(2)),
          child: child!,
        ),
        home: Scaffold(
          body: SingleChildScrollView(
            padding: const EdgeInsets.all(OpenNetworkSpacing.four),
            child: Column(
              children: [
                const Text('NDDev OpenNetwork · Устройства и серверы'),
                const TextField(
                  decoration: InputDecoration(labelText: 'Email / Почта'),
                ),
                FilledButton(
                  onPressed: () {},
                  child: const Text('Continue / Продолжить'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
    await tester.tap(find.byType(TextField));
    await tester.pump();
    expect(tester.takeException(), isNull);
    expect(find.text('Continue / Продолжить'), findsOneWidget);
  });
}

double contrast(Color a, Color b) {
  final luminance = [a.computeLuminance(), b.computeLuminance()]..sort();
  return (luminance.last + 0.05) / (luminance.first + 0.05);
}
