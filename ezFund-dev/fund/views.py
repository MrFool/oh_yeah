from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Fund


from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from operator import itemgetter, attrgetter


@login_required(login_url='/admin/')
def index(request):
    now_user = request.user
    if now_user.has_perm(perm="fund.student_approve"):
        show_add_button = False
        fund_objects = Fund.objects.all()
    else:
        if now_user.has_perm(perm="fund.teacher_approve"):
            show_add_button = False
            #ground_list = Fund.objects.filter(is_viewed_by_student=True)
            #fund_objects = ground_list.objects.filter(is_objected=False)
            fund_objects = Fund.objects.filter(is_objected=False, is_viewed_by_student=True)
        else:
            if now_user.hasperm(perm="fund.apply_only"):
                show_add_button = True
                fund_objects = Fund.objects.all()
    fund_list = sorted(fund_objects, key=attrgetter('id'), reverse=True)
    paginator = Paginator(fund_list,10)
    page = request.GET.get('page')
    try:
        fund_list = paginator.page(page)
    except PageNotAnInteger:
        fund_list = paginator.page(1)
    except EmptyPage:
        fund_list = paginator.page(paginator.num_pages)
    context = {
        'show_add_button': show_add_button,
        'username': request.user.username,
        'fund_list': fund_list,
        'now_user': now_user,
    }
    return render(request, 'index.html', context)


@login_required(login_url='/admin/')
def detail(request, fund_id):
    fund = get_object_or_404(Fund, pk=fund_id)
    content = {
        'username': request.user.username,
        'fund': fund,
        'fund_stat': fund.fund_status(),
    }
    return render(request, 'detail.html', content)


@login_required(login_url='/admin/')
def approve(request, fund_id):
    now_user = request.user
    if now_user.has_perm(perm="fund.student_approve"):
        app_fund = get_object_or_404(Fund, pk=fund_id)
        app_fund.is_viewed_by_student = True
        app_fund.save()
    else:
        if now_user.has_perm(perm="fund.teacher_approve"):
            app_fund = get_object_or_404(Fund, pk=fund_id)
            app_fund.is_viewed_by_teacher = True
            app_fund.save()
    return detail(request, fund_id)


@login_required(login_url='/admin/')
def deny(request, fund_id):
    now_user = request.user
    if now_user.has_perm(perm="fund.student_approve"):
        app_fund = get_object_or_404(Fund, pk=fund_id)
        app_fund.is_viewed_by_student = True
        app_fund.is_objected = True
        app_fund.save()
    else:
        if now_user.has_perm(perm="fund.teacher_approve"):
            app_fund = get_object_or_404(Fund, pk=fund_id)
            app_fund.is_viewed_by_teacher = True
            app_fund.is_objected = True
            app_fund.save()
    return detail(request, fund_id)





