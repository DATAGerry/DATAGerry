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

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavigationComponent } from './structure/navigation/navigation.component';
import { RouterModule } from '@angular/router';
import { BreadcrumbComponent } from './structure/breadcrumb/breadcrumb.component';
import { BreadcrumbService } from './structure/breadcrumb/breadcrumb.service';
import { SidebarComponent } from './structure/sidebar/sidebar.component';
import { SidebarCategoryComponent } from './structure/sidebar/sidebar-category.component';
import { ContentHeaderComponent } from './components/content-header/content-header.component';
import { ActiveBadgeComponent } from './helpers/active-badge/active-badge.component';
import { LowercaseDirective } from './directives/lowercase.directive';
import { SearchBarComponent } from './components/search-bar/search-bar.component';
import { FooterComponent } from './structure/footer/footer.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { TableComponent } from './components/table/table.component';
import { DataTablesModule } from 'angular-datatables';
import { NgbActiveModal, NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ModalComponent } from './helpers/modal/modal.component';
import { TableModule } from './components/table/table.module';
import { TypeLabelComponent } from './helpers/type-label/type-label.component';
import { SweetAlert2Module } from '@sweetalert2/ngx-sweetalert2';

import { FaIconLibrary, FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';
import { fab } from '@fortawesome/free-brands-svg-icons';
import { IconPickerModule } from 'ngx-icon-picker';
import { IconPickerComponent } from './helpers/icon-picker/icon-picker.component';
import { UserImageComponent } from './components/user-image/user-image.component';
import { UserDisplayComponent } from './components/user-display/user-display.component';
import { ChartsComponent } from './components/charts/charts.component';
import { ToastModule } from './toast/toast.module';
import { AuthModule } from '../auth/auth.module';

@NgModule({
  declarations: [
    LowercaseDirective,
    BreadcrumbComponent,
    NavigationComponent,
    SidebarComponent,
    SidebarCategoryComponent,
    ContentHeaderComponent,
    ActiveBadgeComponent,
    SearchBarComponent,
    TableComponent,
    ModalComponent,
    TypeLabelComponent,
    FooterComponent,
    IconPickerComponent,
    UserImageComponent,
    UserDisplayComponent,
    ChartsComponent
  ],
  exports: [
    LowercaseDirective,
    NavigationComponent,
    BreadcrumbComponent,
    FooterComponent,
    ContentHeaderComponent,
    ActiveBadgeComponent,
    SearchBarComponent,
    TableComponent,
    TypeLabelComponent,
    IconPickerComponent,
    UserImageComponent,
    UserDisplayComponent,
    ChartsComponent,
  ],
  imports: [
    CommonModule,
    RouterModule,
    NgSelectModule,
    ReactiveFormsModule,
    NgbModule,
    FormsModule,
    DataTablesModule,
    TableModule,
    SweetAlert2Module.forRoot({
      buttonsStyling: false,
      customClass: 'modal-content',
      confirmButtonClass: 'btn btn-primary',
      cancelButtonClass: 'btn'
    }),
    FontAwesomeModule,
    IconPickerModule,
    ToastModule,
    AuthModule
  ],
  providers: [
    BreadcrumbService,
    NgbActiveModal
  ],
  entryComponents: [
    ModalComponent
  ]
})
export class LayoutModule {
  constructor(private iconLibrary: FaIconLibrary) {
    iconLibrary.addIconPacks(fas, far, fab);
  }
}
