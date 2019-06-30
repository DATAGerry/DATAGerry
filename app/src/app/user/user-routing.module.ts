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

import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { NavigationComponent } from '../layout/components/navigation/navigation.component';
import { SidebarComponent } from '../layout/components/sidebar/sidebar.component';
import { BreadcrumbComponent } from '../layout/components/breadcrumb/breadcrumb.component';
import { FooterComponent } from '../layout/components/footer/footer.component';
import { UserViewComponent } from './components/user-view/user-view.component';

const routes: Routes = [
  {
    path: '',
    component: NavigationComponent,
    outlet: 'navigation'
  },
  {
    path: '',
    component: SidebarComponent,
    outlet: 'sidebar'
  },
  {
    path: '',
    component: BreadcrumbComponent,
    outlet: 'breadcrumb'
  },
  {
    path: '',
    component: FooterComponent,
    outlet: 'footer'
  },
  {
    path: '',
    data: {
      breadcrumb: 'User'
    },
    component: UserViewComponent
  },
  {
    path: ':publicID',
    data: {
      breadcrumb: 'View'
    },
    component: UserViewComponent
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule {
}
