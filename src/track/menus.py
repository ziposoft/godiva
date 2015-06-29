from django.core.urlresolvers import reverse

from menu import Menu, MenuItem



submenu_track = (
    MenuItem("Events",
             reverse("track:events"),
             weight=10,
             icon="user"),
    MenuItem("Runners",
             reverse("track:runners"),
             weight=10,
             separator=True,
             icon="user"),
    MenuItem("By Year",
             reverse("track:year"),
             weight=10,
             icon="user"),

)


Menu.add_item("main", MenuItem("Track",
                               reverse("track:index"),
                               children=submenu_track
                               ))

Menu.add_item("main", MenuItem("Results",
                               reverse("track:results"),
                               #check=lambda request: request.user.is_staff
                                ))

Menu.add_item("main", MenuItem("Superuser Only",
                               reverse("track:index"),
                               check=lambda request: request.user.is_superuser))
