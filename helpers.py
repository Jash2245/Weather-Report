class WeatherVisualizer:
    @staticmethod
    def format_summary(summary: Dict) -> str:
        """Format daily summary as a string."""
        return (
            f"Weather Summary for {summary['date']}\n"
            f"-------------------------\n"
            f"Average Temperature: {summary['avg_temperature']:.1f}°C\n"
            f"Maximum Temperature: {summary['max_temperature']:.1f}°C\n"
            f"Minimum Temperature: {summary['min_temperature']:.1f}°C\n"
            f"Dominant Condition: {summary['dominant_condition']} "
            f"({summary['condition_frequency']} of the day)\n"
            f"Number of Samples: {summary['samples_count']}"
        )