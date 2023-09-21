/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, OnDestroy, OnInit, Renderer2 } from '@angular/core';

import * as jQuery from 'jquery';

import { AuthService } from '../../../auth/services/auth.service';
import { UserService } from '../../../management/services/user.service';
import { GroupService } from '../../../management/services/group.service';

import { User } from '../../../management/models/user';
import { Group } from '../../../management/models/group';
/* ------------------------------------------------------------------------------------------------------------------ */


declare global {
  interface Window { ATL_JQ_PAGE_PROPS: any; }
}

window.ATL_JQ_PAGE_PROPS = window.ATL_JQ_PAGE_PROPS || {};

@Component({
  selector: 'cmdb-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent implements OnInit, OnDestroy {

  public readonly title: string = 'DATAGERRY';
  public user: User;
  public group: Group;

  constructor(private renderer: Renderer2, 
              public authService: AuthService, 
              private userService: UserService,
              private groupService: GroupService) {

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

    jQuery.ajax({
      url: "https://becon88.atlassian.net/s/d41d8cd98f00b204e9800998ecf8427e-T/6i46lu/b/8/b0105d975e9e59f24a3230a22972a71a/_/download/batch/com.atlassian.jira.collector.plugin.jira-issue-collector-plugin:issuecollector-embededjs/com.atlassian.jira.collector.plugin.jira-issue-collector-plugin:issuecollector-embededjs.js?locale=de-DE&collectorId=f2da5b6f",
      type: 'get',
      cache: true,
      dataType: 'script'
    });

    window.ATL_JQ_PAGE_PROPS =  {
      "triggerFunction": function(showCollectorDialog) {
        showCollectorDialog();
      }
    };
  }


  public openIntroModal(){
    this.authService.showIntro();
  }

}
