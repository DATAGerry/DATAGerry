/*
* dataGerry - OpenSource Enterprise CMDB
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
import { ApiCallService } from '../../../services/api-call.service';

@Component({
  selector: 'cmdb-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit, OnDestroy {
  public categoryTree: any;
  constructor(private api: ApiCallService, private renderer: Renderer2) { }

  public ngOnInit(): void {
    this.renderer.addClass(document.body, 'sidebar-fixed');
    const categoryTreeObserver = this.api.callGetRoute('category/tree');
    categoryTreeObserver.subscribe(tree => {
      this.categoryTree = tree;
    });
  }

  public ngOnDestroy(): void {
    this.renderer.removeClass(document.body, 'sidebar-fixed');
  }

}
