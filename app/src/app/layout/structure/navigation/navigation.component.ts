/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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
import { UserService } from '../../../management/services/user.service';
import { User } from '../../../management/models/user';
import { GroupService } from '../../../management/services/group.service';
import { Group } from '../../../management/models/group';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { FeedbackModalComponent } from '../../helpers/modals/feedback-modal/feedback-modal.component';

@Component({
  selector: 'cmdb-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent implements OnInit, OnDestroy {

  public readonly title: string = 'DATAGERRY';
  public user: User;
  public group: Group;

  constructor(private renderer: Renderer2, public authService: AuthService, private userService: UserService,
              private groupService: GroupService, private modalService: NgbModal) {
    this.user = this.userService.getCurrentUser();
  }

  public ngOnInit(): void {
    this.groupService.getGroup(this.user.group_id).subscribe(resp => {
      this.group = resp;
    });
    this.renderer.addClass(document.body, 'header-fixed');
    this.dropdownSubmenu();
  }

  public ngOnDestroy(): void {
    this.renderer.removeClass(document.body, 'header-fixed');
  }

  public logout(): void {
    this.authService.logout();
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

  public feedback() {
    const modalComponent = this.modalService.open(FeedbackModalComponent, {size: 'xl'});
    return modalComponent.result;
  }
}
