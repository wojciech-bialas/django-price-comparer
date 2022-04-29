from .models import DatesWhenScraperRun, ProductPrice
from django.db.models import Q
import io, base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Chart:

    def draw_cat_chart(self, category):
        run_dates = DatesWhenScraperRun.objects.all()
        avg_per_day = []
        dates = []
        for rd in run_dates:

            # get a list of all prices from one category at given day
            prices = list(ProductPrice.objects.filter(
                Q(date=rd.date) & Q(product_offer__product__category=category)
                ).values_list('price', flat=True))

            # not all categories were scraped from the beggining, hence skipping
            if len(prices) == 0:
                continue

            avg_per_day.append(sum(prices) / len(prices))
            dates.append(rd.date)
            
        fig, ax = plt.subplots(figsize=(10,3))
        ax = plt.plot(dates, avg_per_day)
        flike = io.BytesIO()
        fig.savefig(flike)
        chart = base64.b64encode(flike.getvalue()).decode()
        return chart

    def make_all_cat_charts(self):
        charts = {
            'gpu': self.draw_cat_chart('gpu'),
            'cpu': self.draw_cat_chart('cpu'),
            'ram': self.draw_cat_chart('ram')
        }
        return charts