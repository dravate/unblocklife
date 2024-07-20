from django.shortcuts import render
from wagtail.admin.panels import FieldPanel
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from courses.models import CoursePage, CoursePageFilterSet


class CoursePageViewSet(SnippetViewSet):
    model = CoursePage 
    icon = "user"
    list_display = ["name", "shirt_size", "get_shirt_size_display", UpdatedAtColumn()]
    list_per_page = 50
    copy_view_enabled = False
    inspect_view_enabled = True
    admin_url_namespace = "courses_views"
    base_url_path = "pages/courses"
    filterset_class = CoursePageFilterSet

    edit_handler = TabbedInterface([
        ObjectList([FieldPanel("name")], heading="Details"),
        ObjectList([FieldPanel("start_date")], heading="Preferences"),
    ])

register_snippet(CoursePageViewSet)
