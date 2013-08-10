from django.db.models import F
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from shortener.baseconv import base62
from shortener.models import Link, URLTags, TagList, Referrer
from shortener.forms import LinkSubmitForm, AddTagForm, TagURLForm

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
    
    # JPK: Add code here to record the referrer and IP address
    
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
    lsform = LinkSubmitForm(request.POST)
    tagform = AddTagForm()
    tagurlform = TagURLForm()

    if lsform.is_valid():
        kwargs = {'url': lsform.cleaned_data['url']}
        custom = lsform.cleaned_data['custom']
        if custom:
            # specify an explicit id corresponding to the custom url
            kwargs.update({'id': base62.to_decimal(custom)})
        link = Link.objects.create(**kwargs)
        
        # JPK Need to put session info here, in the list that is
        # passed to the form

        request.session['link_id'] = link.id        
        
        return render(request, 'shortener/submit_success.html', {'link': link; 'tag_form': tagform; 'tag_select_form': tagurlform })
    else:
        return render(request, 'shortener/submit_failed.html', {'link_form': lsform})


@require_POST
def addtag(request):
    """
    The view for adding tags to a particular URL.
    """

    # Where do we get the link?  From the session.  Then
    
    link = request.session['link_id']

    form1 = AddTagForm(request)
    AddTagForm.link = link.id
    
    if form1.is_valid():
        # If we get here, that means the user entered a tag
        # in the 'new tag' field, so that we have to add
        # the tag to the tag table before we attach it to
        # the URL.  Multiple tags allowed, separated by a
        # semicolon.
        multiple_tags = form1.tag_text.split(';')
        # kwargs = {'url': lsform.cleaned_data['url']}
        # kwargs.update({'id': base62.to_decimal(custom)})
        # link = Link.objects.create(**kwargs)
        
        for one_tag in multiple_tags:
            misc_tag = Tag.objects.create('tag_text': one_tag)
                
        pass
        
    form2 = TagURLForm(request)
    if form2.is_valid():
        # If we get here, the user also selected tag(s) from the
        # multi-select list.
        
        # Attach the tags to the URL.  For each item returned by
        # the multi-select list, add a URLTags object.
        
        # What's the name of the multi-select object?
        for item in form2.multiselectobject.getlist(''):

            # Did the user actually select a tag?  We can get a
            # valid form back if only the first item, which is
            # the label for the multi-select, is selected.
            if item = 'Select a Tag':
                break
            
            # Nope, if we get here there are tags selected.
    
    
        pass

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
