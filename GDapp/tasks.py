from GDapp.models import GoldParticleDataImage, get_data_dict
from run import run_gold_digger
from GDapp.prediction.FrontEndUpdater import FrontEndUpdater
from celery import shared_task
import time


@shared_task(bind=True)
def celery_timer_task(self, pk):
    print(pk)
    feu = FrontEndUpdater(pk)
    time.sleep(5)
    feu.update(10, "update from celery timer task")
    return ('Done')


@shared_task(bind=True)
def run_gold_digger_task(self, pk):
    print(pk)
    # obj = GoldParticleDataImage.objects.get(pk=pk)
    data = get_data_dict(pk)

    # if obj.mask.name == '':
    #     mask = None
    # else:
    #     mask = obj.mask.path
    front_end_updater = FrontEndUpdater(pk)
    if data['mask'].name == '':
        mask = None
    else:
        mask = data['mask'].path
    try:
        run_gold_digger(
            data['trained_model'],
            data['image'].path,
            data['particle_groups'],
            mask, 
            front_end_updater,
        )

        # run_gold_digger(obj.trained_model, obj.image.path, obj.particle_groups, mask, front_end_updater)
    except Exception as e:
        front_end_updater.error_message(str(e))
