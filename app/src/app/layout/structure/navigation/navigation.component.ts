/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, OnDestroy, OnInit, Renderer2 } from '@angular/core';
import { AuthService } from '../../../auth/services/auth.service';
import { Router } from '@angular/router';
import {SystemService} from '../../../settings/system/system.service';

@Component({
  selector: 'cmdb-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent implements OnInit, OnDestroy {

  public readonly title: string = 'DATAGERRY';

  constructor(private renderer: Renderer2, public authService: AuthService, private router: Router) {
  }

  public ngOnInit(): void {
    this.renderer.addClass(document.body, 'header-fixed');
    this.dropdownSubmenu();
  }

  public ngOnDestroy(): void {
    this.renderer.removeClass(document.body, 'header-fixed');
  }

  public logout(): void {
    this.authService.logout();
    this.router.navigate(['/auth']);
  }

  private dropdownSubmenu() {
    $('.dropdown-menu a.dropdown-toggle').on('click', (e) => {
      if (!$(this).next().hasClass('show')) {
        $(this).parents('.dropdown-menu').first().find('.show').removeClass('show');
      }
      const $subMenu = $(this).next('.dropdown-menu');
      $subMenu.toggleClass('show');
      // tslint:disable-next-line:only-arrow-functions
      $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', () => {
        $('.dropdown-submenu .show').removeClass('show');
      });
      return false;
    });
  }

  public visibilitySidebar() {
    const sidebar = document.getElementById('sidebar').classList;
    sidebar.length === 0 ? sidebar.add('set-sidebar-visible') : sidebar.remove('set-sidebar-visible');
  }
}
