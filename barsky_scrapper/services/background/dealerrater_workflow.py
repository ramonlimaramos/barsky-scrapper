from celery import shared_task, group


__all__ = ['dealerrater_workflow']


@shared_task(bind=True)
def dealerrater_workflow(self):
    workflow = (get_dealer_rater_data.s() |
                render_it_json_format.s() |
                analyse_with_nlu.s() |
                format_and_save_response.s())

    return workflow.apply_async()


@shared_task(bind=True)
def get_dealer_rater_data(self, args, **kwargs):
    return 1


@shared_task(bind=True)
def render_it_json_format(self, args, **kwargs):
    return 1


@shared_task(bind=True)
def analyse_with_nlu(self, args, **kwargs):
    return 1


@shared_task(bind=True)
def format_and_save_response(self, args, **kwargs):
    return 1
