"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - SURFACE
Test Surface widget.
"""

__all__ = ['SurfaceWidgetTest']

from test._utils import MenuUtils, surface, PygameEventUtils, BaseTest
import pygame

import pygame_menu
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented


class SurfaceWidgetTest(BaseTest):

    def test_surface_widget(self) -> None:
        """
        Test surface widget.
        """
        menu = MenuUtils.generic_menu()
        surf = pygame.Surface((150, 150))
        surf.fill((255, 192, 203))
        surf_widget = menu.add.surface(surf, font_color='red')

        self.assertEqual(surf_widget.get_size(), (166, 158))
        self.assertEqual(surf_widget.get_size(apply_padding=False), (150, 150))
        self.assertEqual(surf_widget.get_surface(), surf)
        self.assertEqual(surf_widget._font_color, (70, 70, 70, 255))  # not red

        self.assertRaises(WidgetTransformationNotImplemented, lambda: surf_widget.rotate(10))
        self.assertEqual(surf_widget._angle, 0)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: surf_widget.resize(10, 10))
        self.assertFalse(surf_widget._scale[0])
        self.assertEqual(surf_widget._scale[1], 1)
        self.assertEqual(surf_widget._scale[2], 1)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: surf_widget.scale(100, 100))
        self.assertFalse(surf_widget._scale[0])
        self.assertEqual(surf_widget._scale[1], 1)
        self.assertEqual(surf_widget._scale[2], 1)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: surf_widget.flip(True, True))
        self.assertFalse(surf_widget._flip[0])
        self.assertFalse(surf_widget._flip[1])

        self.assertRaises(WidgetTransformationNotImplemented, lambda: surf_widget.set_max_width(100))
        self.assertIsNone(surf_widget._max_width[0])

        self.assertRaises(WidgetTransformationNotImplemented, lambda: surf_widget.set_max_height(100))
        self.assertIsNone(surf_widget._max_height[0])

        surf_widget.set_title('epic')
        self.assertEqual(surf_widget.get_title(), '')

        new_surface = pygame.Surface((160, 160))
        new_surface.fill((255, 192, 203))
        inner_surface = pygame.Surface((80, 80))
        inner_surface.fill((75, 0, 130))
        new_surface.blit(inner_surface, (40, 40))
        surf_widget.set_surface(new_surface)
        self.assertEqual(surf_widget.get_size(apply_padding=False), (160, 160))
        menu.draw(surface)
        surf_widget.update(PygameEventUtils.mouse_motion(surf_widget))
        surf_widget.draw(surface)

    def test_value(self) -> None:
        """
        Test surface value.
        """
        menu = MenuUtils.generic_menu()
        surf = menu.add.surface(pygame.Surface((150, 150)))
        self.assertRaises(ValueError, lambda: surf.get_value())
        self.assertRaises(ValueError, lambda: surf.set_value('value'))
        self.assertFalse(surf.value_changed())
        surf.reset_value()

    def test_fit_to_menu(self) -> None:
        """
        Test SurfaceWidget.fit_to_menu resizing behavior.
        """
        menu = MenuUtils.generic_menu()  # Default size: 600x600
        original_surface = pygame.Surface((300, 100))  # Aspect ratio: 3.0
        widget = menu.add.surface(original_surface)
    
        # Check original size before fitting
        self.assertEqual(widget.get_size(apply_padding=False), (300, 100))
    
        widget.fit_to_menu()
    
        # After fit_to_menu, surface should be resized to match inner menu size proportionally
        menu_width, menu_height = menu.get_size(inner=True)
        target_ratio = 3.0
    
        if menu_width / menu_height < target_ratio:
            expected_width = menu_width
            expected_height = int(menu_width / target_ratio)
        else:
            expected_height = menu_height
            expected_width = int(menu_height * target_ratio)
    
        actual_width, actual_height = widget.get_size(apply_padding=False)
        self.assertEqual((actual_width, actual_height), (expected_width, expected_height))
    
        # Draw and update to ensure no crash
        menu.draw(surface)
        widget.update(PygameEventUtils.mouse_motion(widget))
        widget.draw(surface)

    def test_fit_to_menu_variants(self) -> None:
        """
        Test fit_to_menu across diverse surface sizes and menu dimensions.
        """
        # Case 1: Wide surface on square menu
        menu1 = MenuUtils.generic_menu(width=500, height=500)
        surface1 = pygame.Surface((400, 100))  # Aspect ratio: 4.0
        widget1 = menu1.add.surface(surface1)
        widget1.fit_to_menu()
        w1, h1 = widget1.get_size(apply_padding=False)
        self.assertTrue(w1 <= 500 and h1 <= 500)
    
        # Case 2: Tall surface on wide menu
        menu2 = MenuUtils.generic_menu(width=600, height=400)
        surface2 = pygame.Surface((100, 300))  # Aspect ratio: 0.33
        widget2 = menu2.add.surface(surface2)
        widget2.fit_to_menu()
        w2, h2 = widget2.get_size(apply_padding=False)
        self.assertTrue(w2 <= 600 and h2 <= 400)
    
        # Case 3: Perfect fit (already matches menu ratio)
        menu3 = MenuUtils.generic_menu(width=400, height=200)
        surface3 = pygame.Surface((200, 100))  # Aspect ratio: 2.0
        widget3 = menu3.add.surface(surface3)
        widget3.fit_to_menu()
        w3, h3 = widget3.get_size(apply_padding=False)
        expected_size = menu3.get_size(inner=True)
        surf_w, surf_h = surface3.get_size()
        expected_h = expected_size[1]
        expected_w = int(expected_h * (surf_w / surf_h))
        self.assertEqual((w3, h3), (expected_w, expected_h))
    
        # Case 4: Tiny surface scaling up
        menu4 = MenuUtils.generic_menu(width=300, height=300)
        surface4 = pygame.Surface((30, 30))
        widget4 = menu4.add.surface(surface4)
        widget4.fit_to_menu()
        w4, h4 = widget4.get_size(apply_padding=False)
        self.assertTrue(w4 > 30 and h4 > 30)
    
        # Case 5: Widget not yet attached to menu (safe fallback)
        surface5 = pygame.Surface((100, 100))
        widget5 = pygame_menu.widgets.SurfaceWidget(surface5)
        widget5.fit_to_menu()  # Should not raise
        self.assertEqual(widget5.get_size(apply_padding=False), (100, 100))
