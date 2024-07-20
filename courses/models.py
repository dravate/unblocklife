from django.db import models
from wagtail.models import Page
from django.shortcuts import redirect, render
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from home.blocks import BaseStreamBlock, TrainerBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.filters import WagtailFilterSet


class CoursesIndexPage(RoutablePageMixin, Page):
    max_count=1
    summary = models.CharField(blank=True, max_length=255)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and 3000px.",
    )

    template = "courses/courses_index_page.html" 

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        FieldPanel("image")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['course_entries'] = CoursesPage.objects.child_of(self).live().order_by('-date')
        return context

    subpage_types = ["CoursesPage"]
  
    def children(self):
        return self.get_children().specific().live()

    @route(r"^tags/$", name="tag_archive")
    @route(r"^tags/([\w-]+)/$", name="tag_archive")
    def tag_archive(self, request, tag=None):
        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no Course  Pagess tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)
        course_entries = self.get_posts(tag=tag)
        context = {"self": self, "tag": tag, "course_entries": course_entries}
        return render(request, "courses/courses_index_page.html", context)

    def serve_preview(self, request, mode_name):
        return self.serve(request)

    # Returns the child CoursePage objects for this CoursePageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self, tag=None):
        posts = CoursesPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts
    # Returns the list of Tags for all child posts of this CoursePage.
    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            # Not tags.append() because we don't want a list of lists
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags



class CoursesPageTag(TaggedItemBase):
    """
    This model allows us to create a many-to-many relationship between
    the CoursePage object and tags. There's a longer guide on using it at
    https://docs.wagtail.org/en/stable/reference/pages/model_recipes.html#tagging
    """

    content_object = ParentalKey(
        "CoursesPage", related_name="tagged_items", on_delete=models.CASCADE
    )






class CoursesPage(Page):
    author = models.CharField(max_length=255)
    date = models.DateField("Post date")
    summary = models.CharField(max_length=1000)
    start_date = models.DateField(null=True, help_text="Schedule Start Date")
    end_date = models.DateField( null=True, help_text="Schedule End Date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField( BaseStreamBlock(), verbose_name="Page body", blank=True, use_json_field=True)
    trainers = StreamField( TrainerBlock(), verbose_name="Trainers", blank=True, use_json_field=True)

    tags = ClusterTaggableManager(through=CoursesPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('summary'),
        index.SearchField('author'),
        index.SearchField('body'),
        index.SearchField('trainers'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('trainers'),
        FieldPanel('date'),
        FieldPanel('summary'),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
        FieldPanel('body'),
        FieldPanel('author'),
        FieldPanel("tags"),
    ]
    panels = [
        FieldPanel('start_date'),
    ]


    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('feed_image'),
    ]
  
    @property
    def get_tags(self):
        """
        Similar to the authors function above we're returning all the tags that
        are related to the course page into a list we can access on the template.
        We're additionally adding a URL to access CoursePage objects with that tag
        """
        tags = self.tags.all()
        base_url = self.get_parent().url
        for tag in tags:
            tag.url = f"{base_url}tags/{tag.slug}/"
        return tags
    
    # Specifies parent to CoursePage as being CourseIndexPages
    parent_page_types = ["CoursesIndexPage"]

    # Specifies what content types can exist as children of CoursePage.
    # Empty list means that no child content types are allowed.
    subpage_types = []

class CoursesPageFillterSet(WagtailFilterSet):
    class Meta:
        model = CoursesPage 
        fields = ["start_date"]
