import 'package:flutter/material.dart';

class ArchitectureInfoPage extends StatelessWidget {
  const ArchitectureInfoPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Architecture Flow')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Clean Architecture + Features',
              style: Theme.of(
                context,
              ).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),
            _buildLayerCard(
              context,
              'Presentation Layer (UI)',
              'Displays data and captures user events. Contains Pages, Widgets, and BLoC/Cubit state management.',
              Colors.blue.shade100,
            ),
            const Icon(Icons.arrow_downward, size: 32, color: Colors.grey),
            _buildLayerCard(
              context,
              'Domain Layer (Business Logic)',
              'Independent of any framework. Contains Entities, Use Cases, and Repository Interfaces.',
              Colors.green.shade100,
            ),
            const Icon(Icons.arrow_downward, size: 32, color: Colors.grey),
            _buildLayerCard(
              context,
              'Data Layer (External/Internal APIs)',
              'Fetches and parses data. Contains Models, Repository Implementations, and Data Sources.',
              Colors.orange.shade100,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLayerCard(
    BuildContext context,
    String title,
    String description,
    Color color,
  ) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.black12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
          ),
          const SizedBox(height: 8),
          Text(description),
        ],
      ),
    );
  }
}
