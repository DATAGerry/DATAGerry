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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FaIconLibrary, FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';
import { fab } from '@fortawesome/free-brands-svg-icons';
import { BreadcrumbService } from './structure/breadcrumb/breadcrumb.service';
import { NavigationComponent } from './structure/navigation/navigation.component';
import { BreadcrumbComponent } from './structure/breadcrumb/breadcrumb.component';
import { IconPickerComponent } from './helpers/icon-picker/icon-picker.component';
import { ChartsComponent } from './components/charts/charts.component';
import { IntroComponent } from './intro/intro.component';
import { StepByStepIntroComponent } from './intro/step-by-step-intro/step-by-step-intro.component';
import { JwPaginationComponent } from 'jw-angular-pagination';
import { SidebarTypeComponent } from './structure/sidebar/sidebar-type.component';
import { TypeLabelComponent } from './helpers/type-label/type-label.component';
import { FooterComponent } from './structure/footer/footer.component';
import { SidebarComponent } from './structure/sidebar/sidebar.component';
import { SidebarCategoryComponent } from './structure/sidebar/sidebar-category.component';
import { ContentHeaderComponent } from './components/content-header/content-header.component';
import { ActiveBadgeComponent } from './helpers/active-badge/active-badge.component';
import { AddAttachmentsModalComponent } from './helpers/modals/add-attachments-modal/add-attachments-modal.component';
import { GeneralModalComponent } from './helpers/modals/general-modal/general-modal.component';
import { ObjectPreviewModalComponent } from '../framework/object/modals/object-preview-modal/object-preview-modal.component';
import { InfoBoxComponent } from './components/info-box/info-box.component';
import { FilemanagerModalComponent } from './helpers/modals/filemanager-modal/filemanager-modal.component';
import { FileExplorerComponent } from './components/file-explorer/fileexplorer.component';
import { FolderTreeComponent } from './components/file-explorer/components/folder-tree/folder-tree.component';
import {
  FileViewListComponent,
} from './components/file-explorer/components/file-view-list/file-view-list.component';
import { NewFolderDialogComponent } from './components/file-explorer/modal/new-folder-dialog/new-folder-dialog.component';
import { RenameDialogComponent } from './components/file-explorer/modal/rename-dialog/rename-dialog.component';
import { ContextmenuComponent } from './components/file-explorer/components/contextmenu/contextmenu.component';
import { FolderPathViewerComponent } from './components/file-explorer/components/folder-path-viewer/folder-path-viewer.component';
import { MoveDialogComponent } from './components/file-explorer/modal/move-dialog/move-dialog.component';
import { MetadataInfoComponent } from './components/file-explorer/modal/metadata-info/metadata-info.component';
import { AttachmentsListModalComponent } from './helpers/modals/attachments-list-modal/attachments-list-modal.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { SearchBarModule } from '../search/search-bar/search-bar.module';
import { ToastModule } from './toast/toast.module';
import { AuthModule } from '../auth/auth.module';
import { IconPickerModule } from 'ngx-icon-picker';
import { NgbActiveModal, NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { RenderModule } from '../framework/render/render.module';
import { FileexplorerModule } from './components/file-explorer/fileexplorer.module';
import { FileDragDropDirective } from './directives/fileDragDrop.directive';
import { NameDirective } from './directives/name.directive';
import { LowercaseDirective } from './directives/lowercase.directive';
import { TableSortEventDirective } from './components/file-explorer/directives/tabletSortEvent.directive';
import { FileSizePipe } from './pipes/file-size.pipe';
import { NameGuidePipe } from './pipes/name-guide.pipe';
import { FileExtensionPipe } from './pipes/file-extension.pipe';
import { CategoryTreeFilterPipe } from './pipes/categoryTreeFilter.pipe';
import { TypeFilterPipe } from './pipes/typeFilter.pipe';
import { TableModule } from './table/table.module';
import { QRCodeModule } from 'angularx-qrcode';
import { QrCodeComponent } from './helpers/qrcode/qr-code.component';
import { FeedbackFormComponent } from './components/feedback-form/feedback-form.component';
import { BlockComponent } from './components/block/block.component';

@NgModule({
  declarations: [
    LowercaseDirective,
    BreadcrumbComponent,
    NavigationComponent,
    SidebarComponent,
    SidebarCategoryComponent,
    ContentHeaderComponent,
    ActiveBadgeComponent,
    GeneralModalComponent,
    IntroComponent,
    TypeLabelComponent,
    FooterComponent,
    IconPickerComponent,
    ChartsComponent,
    StepByStepIntroComponent,
    JwPaginationComponent,
    NameDirective,
    NameGuidePipe,
    FileDragDropDirective,
    FileSizePipe,
    SidebarTypeComponent,
    CategoryTreeFilterPipe,
    TypeFilterPipe,
    FileExtensionPipe,
    AddAttachmentsModalComponent,
    FilemanagerModalComponent,
    GeneralModalComponent,
    ObjectPreviewModalComponent,
    InfoBoxComponent,
    FileExplorerComponent,
    FolderTreeComponent,
    FileViewListComponent,
    NewFolderDialogComponent,
    RenameDialogComponent,
    MetadataInfoComponent,
    ContextmenuComponent,
    FolderPathViewerComponent,
    MoveDialogComponent,
    TableSortEventDirective,
    AttachmentsListModalComponent,
    QrCodeComponent,
    FeedbackFormComponent,
    BlockComponent
  ],
  exports: [
    FileExplorerComponent,
    LowercaseDirective,
    NavigationComponent,
    BreadcrumbComponent,
    FooterComponent,
    ContentHeaderComponent,
    ActiveBadgeComponent,
    TypeLabelComponent,
    IconPickerComponent,
    ChartsComponent,
    JwPaginationComponent,
    SidebarComponent,
    NameDirective,
    NameGuidePipe,
    FileDragDropDirective,
    FileSizePipe,
    CategoryTreeFilterPipe,
    TypeFilterPipe,
    FileExtensionPipe,
    InfoBoxComponent,
    QrCodeComponent,
    BlockComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    NgSelectModule,
    ReactiveFormsModule,
    SearchBarModule,
    NgbModule,
    FormsModule,
    TableModule,
    FontAwesomeModule,
    IconPickerModule,
    ToastModule,
    AuthModule,
    RenderModule,
    FileexplorerModule,
    QRCodeModule
  ],
  providers: [
    BreadcrumbService,
    NgbActiveModal
  ],
  entryComponents: [
    GeneralModalComponent,
    AddAttachmentsModalComponent,
    AttachmentsListModalComponent,
    FilemanagerModalComponent,
    IntroComponent,
    StepByStepIntroComponent,
    ObjectPreviewModalComponent
  ]
})
export class LayoutModule {
  constructor(private iconLibrary: FaIconLibrary) {
    iconLibrary.addIconPacks(fas, far, fab);
  }
}
