from .models import DatesWhenScraperRun, ProductPrice
from django.db.models import Q
import plotly.graph_objects as go


class Chart:

    def draw_cat_chart(self, category):
        run_dates = DatesWhenScraperRun.objects.all()
        avg_per_day = []
        dates = []

        for rd in run_dates:
            prices = list(ProductPrice.objects.filter(
                Q(date=rd.date) & Q(product_offer__product__category=category)
                ).values_list('price', flat=True))
            
            if len(prices) == 0:
                continue

            avg_per_day.append(sum(prices) / len(prices))
            dates.append(rd.date)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dates,
            y=avg_per_day,
            mode='lines+markers',
            name=f'{category} Średnia cena',
            line=dict(color='royalblue', width=2),
            marker=dict(size=6),
            hovertemplate='<b>Data:</b> %{x}<br><b>Śr. cena:</b> %{y:.2f} PLN<extra></extra>'
        ))

        fig.update_layout(
            title=f'{category.upper()} Trend cenowy w czasie',
            xaxis_title='Data',
            yaxis_title='Średnia Cena (PLN)',
            template='plotly_white',
            xaxis=dict(tickformat="%Y-%m-%d", tickangle=45),
            hovermode="x unified"
        )

        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn', include_mathjax=False, config={'responsive': True})
        
        return chart_html


    def make_all_cat_charts(self):
        charts = {
            'gpu': self.draw_cat_chart('gpu'),
            'cpu': self.draw_cat_chart('cpu'),
            'ram': self.draw_cat_chart('ram')
        }
        return charts

    def get_product_chart(self, offer):
        prices = ProductPrice.objects.filter(product_offer=offer).order_by('date')
        dates = [price.date for price in prices]
        price_values = [price.price for price in prices]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dates,
            y=price_values,
            mode='lines+markers',
            name=f'{offer.product.name} Trend cenowy',
            line=dict(color='green', width=2),
            marker=dict(size=6),
            hovertemplate='<b>Data:</b> %{x}<br><b>Cena:</b> %{y:.2f} PLN<extra></extra>'
        ))

        fig.update_layout(
            title=f'Trend cenowy dla {offer.product.name} w sklepie ({offer.shop})',
            xaxis_title='Data',
            yaxis_title='Cena (PLN)',
            template='plotly_white',
            xaxis=dict(tickformat="%Y-%m-%d", tickangle=45),
            hovermode="x unified"
        )

        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn', include_mathjax=False, config={'responsive': True})
        
        return chart_html
