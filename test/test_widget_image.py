"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - IMAGE
Test Image widget.
"""

import pygame
import pytest

import pygame_menu
from test._utils import MenuUtils, PygameEventUtils, surface


@pytest.fixture
def menu():
    """Create a generic menu fixture for image tests."""
    return MenuUtils.generic_menu()


def test_image_widget_basic(menu):
    """Test image widget."""
    img = menu.add.image(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, font_color=(2, 9)
    )

    img.set_title("epic")
    assert img.get_title() == ""
    assert img.get_image() is img._image

    img.update(PygameEventUtils.mouse_motion(img))

    assert img.get_height(apply_selection=True) == 264
    assert not img._selected
    assert img.get_selected_time() == 0


def test_image_widget_transformations(menu):
    """Test image widget transformations."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    assert img.get_size() == (272, 264)

    img.scale(2, 2)
    assert img.get_size() == (528, 520)

    img.resize(500, 500)
    img.set_padding(0)
    assert img.get_size() == (500, 500)

    # Max width
    img.set_max_width(400)
    assert img.get_size() == (400, 500)

    img.set_max_width(800)
    assert img.get_size() == (400, 500)

    img.set_max_width(300, scale_height=True)
    assert img.get_size() == (300, 375)

    # Max height
    img.set_max_height(400)
    assert img.get_size() == (300, 375)

    img.set_max_height(300)
    assert img.get_size() == (300, 300)

    img.set_max_height(200, scale_width=True)
    assert img.get_size() == (200, 200)

    # Rotation
    assert img.get_angle() == 0
    img.rotate(90)
    assert img.get_angle() == 90
    img.rotate(60)
    assert img.get_angle() == 60

    # Flip
    img.flip(True, True)
    assert img._flip == (True, True)

    img.flip(False, False)
    assert img._flip == (False, False)

    img.draw(surface)


def test_image_widget_value_api(menu):
    """Test image value."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    with pytest.raises(ValueError):
        img.get_value()

    with pytest.raises(ValueError):
        img.set_value("value")

    assert not img.value_changed()
    img.reset_value()


def test_image_from_surface(menu):
    """Test that Image accepts a pygame.Surface and wraps it correctly."""
    surf = pygame.Surface((120, 80))
    img = menu.add.image(surf)
    img.set_padding(0)

    assert isinstance(img.get_image(), pygame_menu.baseimage.BaseImage)
    assert img.get_size() == (120, 80)


def test_image_surface_transformations(menu):
    """Test transformations on an Image created from a pygame.Surface."""
    surf = pygame.Surface((100, 50))
    img = menu.add.image(surf)
    img.set_padding(0)

    img.scale(2, 2)
    assert img.get_size() == (200, 100)

    img.resize(300, 150)
    assert img.get_size() == (300, 150)

    img.rotate(45)
    assert img.get_angle() == 45


def test_image_surface_widget_behavior(menu):
    """Ensure Surface-based Image behaves like a normal widget."""
    surf = pygame.Surface((60, 60))
    img = menu.add.image(surf)

    img.set_padding(10)
    assert img.get_size() == (80, 80)

    img.update(PygameEventUtils.mouse_motion(img))
    assert img._mouseover


def test_image_set_image(menu):
    """Test replacing image object."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    new_img = pygame_menu.baseimage.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU
    )

    img.set_image(new_img)

    assert img.get_image() is new_img
    assert img._surface is not None


def test_image_flip_noop(menu):
    """Flipping False/False should not invalidate the image."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    original_surface = img._surface

    img.flip(False, False)

    assert img._flip == (False, False)
    assert img._surface is original_surface


def test_image_set_max_width_no_resize(menu):
    """set_max_width should do nothing if image is already smaller."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    img.resize(100, 100)

    size_before = img.get_size()

    img.set_max_width(500)

    assert img.get_size() == size_before


def test_image_set_max_height_no_resize(menu):
    """set_max_height should do nothing if image is already smaller."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    img.resize(100, 100)

    size_before = img.get_size()

    img.set_max_height(500)

    assert img.get_size() == size_before


def test_image_deferred_rotate(menu):
    """Deferred rotation should invalidate surface without breaking angle/render."""
    surf = pygame.Surface((200, 100))
    img = menu.add.image(surf)

    old_size = img.get_size()  # (200, 100)

    img.rotate(90, render=False)

    assert img._surface is None
    assert img.get_angle() == 90

    # Drawing should trigger re-render and swap dimensions due to 90° rotation
    img.draw(surface)

    assert img._surface is not None
    assert img.get_size() != old_size


def test_image_deferred_resize(menu):
    """Deferred resize should invalidate without immediate render."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    img.set_padding(0)

    img.resize(400, 250, render=False)

    assert img._surface is None

    # Size information should remain coherent
    assert img.get_size() == (400, 250)

    img.draw(surface)

    assert img._surface is not None
    assert img.get_size() == (400, 250)


def test_image_deferred_scale(menu):
    """Deferred scale should invalidate without immediate render."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    img.set_padding(0)

    img.scale(2, 2, render=False)

    assert img._surface is None

    img.draw(surface)

    assert img._surface is not None


def test_image_deferred_flip(menu):
    """Deferred flip should lazily render."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    img.flip(True, False, render=False)

    assert img._flip == (True, False)
    assert img._surface is None

    img.draw(surface)

    assert img._surface is not None


def test_image_chained_deferred_transformations(menu):
    """Multiple deferred transformations should only require one redraw."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    img.scale(2, 2, render=False)
    img.rotate(45, render=False)
    img.flip(True, False, render=False)

    assert img._surface is None
    assert img.get_angle() == 45
    assert img._flip == (True, False)

    img.draw(surface)

    assert img._surface is not None


def test_image_render_false_updates_size(menu):
    """Deferred operations must still update layout dimensions."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    img.set_padding(0)

    img.resize(200, 100, render=False)

    assert img.get_size() == (200, 100)


def test_image_deferred_set_max_width(menu):
    """Deferred max-width resize should update dimensions."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    img.set_padding(0)

    img.set_max_width(100, render=False)

    assert img._surface is None
    assert img.get_width() == 100

    img.draw(surface)

    assert img._surface is not None


def test_image_deferred_set_max_height(menu):
    """Deferred max-height resize should update dimensions."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    img.set_padding(0)

    img.set_max_height(100, render=False)

    assert img._surface is None
    assert img.get_height() == 100

    img.draw(surface)

    assert img._surface is not None


def test_image_from_baseimage(menu):
    """Image should accept an existing BaseImage."""
    base = pygame_menu.baseimage.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES
    )

    img = menu.add.image(base)

    assert img.get_image() is base


def test_image_widget_id(menu):
    """Image id should be preserved."""
    img = menu.add.image(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
        image_id="test_image",
    )

    assert img.get_id() == "test_image"
