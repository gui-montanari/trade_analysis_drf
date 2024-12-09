from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_risk_per_trade', models.FloatField(default=2.0)),
                ('max_position_size', models.FloatField(default=10.0)),
                ('preferred_leverage', models.IntegerField(default=1)),
                ('notification_email', models.BooleanField(default=True)),
                ('auto_update', models.BooleanField(default=True)),
                ('update_interval', models.IntegerField(default=60)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Configuração do Usuário',
                'verbose_name_plural': 'Configurações dos Usuários',
            },
        ),
        migrations.CreateModel(
            name='TradingSignal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signal_type', models.CharField(choices=[('futures', 'Futures'), ('day', 'Day Trading'), ('swing', 'Swing Trading'), ('position', 'Position Trading')], max_length=10)),
                ('direction', models.CharField(choices=[('buy', 'Compra'), ('sell', 'Venda'), ('neutral', 'Neutro')], max_length=10)),
                ('entry_price', models.DecimalField(decimal_places=8, max_digits=20)),
                ('stop_loss', models.DecimalField(decimal_places=8, max_digits=20)),
                ('take_profit', models.DecimalField(decimal_places=8, max_digits=20)),
                ('confidence', models.FloatField()),
                ('risk_reward', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('success', models.BooleanField(blank=True, null=True)),
                ('market_price', models.DecimalField(decimal_places=8, max_digits=20)),
                ('volume_24h', models.DecimalField(decimal_places=2, max_digits=20)),
                ('change_24h', models.FloatField()),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analysis_type', models.CharField(choices=[('futures', 'Futures'), ('day', 'Day Trading'), ('swing', 'Swing Trading'), ('position', 'Position Trading')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=8, max_digits=20)),
                ('rsi', models.FloatField()),
                ('macd', models.FloatField()),
                ('signal_line', models.FloatField()),
                ('upper_band', models.FloatField()),
                ('lower_band', models.FloatField()),
                ('trend', models.CharField(max_length=20)),
                ('trend_strength', models.FloatField()),
                ('volume', models.DecimalField(decimal_places=2, max_digits=20)),
                ('market_cap', models.DecimalField(decimal_places=2, max_digits=20)),
                ('dominance', models.FloatField()),
                ('recommendation', models.TextField()),
                ('confidence', models.FloatField()),
            ],
            options={
                'verbose_name': 'Análise',
                'verbose_name_plural': 'Análises',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert_type', models.CharField(choices=[('price', 'Preço'), ('indicator', 'Indicador'), ('volume', 'Volume'), ('trend', 'Tendência')], max_length=10)),
                ('condition', models.CharField(choices=[('above', 'Acima'), ('below', 'Abaixo'), ('crosses_up', 'Cruza para Cima'), ('crosses_down', 'Cruza para Baixo')], max_length=12)),
                ('target_value', models.DecimalField(decimal_places=8, max_digits=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('triggered', models.BooleanField(default=False)),
                ('triggered_at', models.DateTimeField(blank=True, null=True)),
                ('notification_sent', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]