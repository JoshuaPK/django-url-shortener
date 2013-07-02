from django.db.models import F
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from shortener.baseconv import base62
from shortener.models import Link, URLTags, TagList, Referrer
from shortener.forms import LinkSubmitForm, AddTagForm

@require_GET
def follow(request, base62_id):
    """
    View which gets the link for the given base62_id value
    and redirects to it.  Also saves information about the
    referrer and IP address that originated the request.
    """
    link = get_object_or_404(Link, id=base62.to_decimal(base62_id))
    link.usage_count = F('usage_count') + 1
    link.save()
    return HttpResponsePermanentRedirect(link.url)


@require_GET
def info(request, base62_id):
    """
    View which shows information on a particular link
    """
    link = get_object_or_404(Link, id=base62.to_decimal(base62_id))
    return render(request, 'shortener/link_info.html', {'link': link})


@require_POST
def submit(request):
    """
    View for submitting a URL to be shortened.  Modified to create a
    session and present that session information in the submit_success
    page so that we can carry the small link from here to the
    add_tag_to_link method.
    """
    form = LinkSubmitForm(request.POST)
    tagform = AddTagForm()
    if form.is_valid():
        kwargs = {'url': form.cleaned_data['url']}
        custom = form.cleaned_data['custom']
        if custom:
            # specify an explicit id corresponding to the custom url
            kwargs.update({'id': base62.to_decimal(custom)})
        link = Link.objects.create(**kwargs)
        
        # JPK Need to put session info here, in the list that is
        # passed to the form

        request.session['link_id'] = link.id        
        
        return render(request, 'shortener/submit_success.html', {'link': link})
    else:
        return render(request, 'shortener/submit_failed.html', {'link_form': form})


@require_POST
def add_tag_to_link(request):

    # Where do we get the link?  From the session.  Then
    
    link = request.session['link_id']

    form = AddTagForm(request)
    AddTagForm.link = link.id

    pass

@require_GET
def index(request):
    """
    View for main page
    """
    values = {
        'link_form': LinkSubmitForm(),
        'recent_links': Link.objects.all().order_by('-date_submitted')[:5],
        'most_popular_links': Link.objects.all().order_by('-usage_count')[:5]}
    return render(request, 'shortener/index.html', values)
