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
import { RouterModule, Routes } from '@angular/router';
import { BreadcrumbComponent } from './structure/breadcrumb/breadcrumb.component';
import { BreadcrumbService } from './structure/breadcrumb/breadcrumb.service';
import { SidebarComponent } from './structure/sidebar/sidebar.component';
import { SidebarCategoryComponent } from './structure/sidebar/sidebar-category.component';
import { ContentHeaderComponent } from './components/content-header/content-header.component';
import { ActiveBadgeComponent } from './helpers/active-badge/active-badge.component';
import { LowercaseDirective } from './directives/lowercase.directive';
import { FooterComponent } from './structure/footer/footer.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { TableComponent } from './components/table/table.component';
import { DataTablesModule } from 'angular-datatables';
import { NgbActiveModal, NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ModalComponent } from './helpers/modal/modal.component';
import { TableModule } from './components/table/table.module';
import { TypeLabelComponent } from './helpers/type-label/type-label.component';

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
import { NgxSpinnerComponent, NgxSpinnerModule } from 'ngx-spinner';
import { LoadingScreenComponent } from './structure/loading-screen/loading-screen.component';
import { SearchBarModule } from '../search/search-bar/search-bar.module';
import { IntroComponent } from './intro/intro.component';
import { StepByStepIntroComponent } from './intro/step-by-step-intro/step-by-step-intro.component';

import { JwPaginationComponent } from 'jw-angular-pagination';
import { NameDirective } from './directives/name.directive';
import { NameGuidePipe } from './pipes/name-guide.pipe';
import { SidebarTypeComponent } from './structure/sidebar/sidebar-type.component';
import { FileDragDropDirective } from './directives/fileDragDrop.directive';
import { FileSizePipe } from './pipes/file-size.pipe';

export const LAYOUT_COMPONENT_ROUTES: Routes = [
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
    component: LoadingScreenComponent,
    outlet: 'loading-screen'
  },
  {
    path: '',
    component: FooterComponent,
    outlet: 'footer'
  }
];

@NgModule({
  declarations: [
    LowercaseDirective,
    BreadcrumbComponent,
    NavigationComponent,
    SidebarComponent,
    SidebarCategoryComponent,
    ContentHeaderComponent,
    ActiveBadgeComponent,
    TableComponent,
    ModalComponent,
    IntroComponent,
    TypeLabelComponent,
    FooterComponent,
    IconPickerComponent,
    UserImageComponent,
    UserDisplayComponent,
    ChartsComponent,
    LoadingScreenComponent,
    StepByStepIntroComponent,
    JwPaginationComponent,
    NameDirective,
    NameGuidePipe,
    FileDragDropDirective,
    FileSizePipe,
    SidebarTypeComponent
  ],
  exports: [
    NgxSpinnerComponent,
    LowercaseDirective,
    NavigationComponent,
    BreadcrumbComponent,
    FooterComponent,
    ContentHeaderComponent,
    ActiveBadgeComponent,
    TableComponent,
    TypeLabelComponent,
    IconPickerComponent,
    UserImageComponent,
    UserDisplayComponent,
    ChartsComponent,
    JwPaginationComponent,
    SidebarComponent,
    NameDirective,
    NameGuidePipe,
    FileDragDropDirective,
    FileSizePipe
  ],
  imports: [
    CommonModule,
    RouterModule,
    NgSelectModule,
    ReactiveFormsModule,
    NgxSpinnerModule,
    SearchBarModule,
    NgbModule,
    FormsModule,
    DataTablesModule,
    TableModule,
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
    ModalComponent,
    IntroComponent,
    StepByStepIntroComponent
  ]
})
export class LayoutModule {
  constructor(private iconLibrary: FaIconLibrary) {
    iconLibrary.addIconPacks(fas, far, fab);
  }
}
