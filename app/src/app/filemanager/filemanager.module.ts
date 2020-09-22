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
import { LayoutModule } from '../layout/layout.module';
import { FilemanagerComponent } from './filemanager.component';
import { FilemanagerRoutingModule } from './filemanager-routing.module';
import { TypeService } from '../framework/services/type.service';
import { ObjectService } from '../framework/services/object.service';
import { FolderTreeComponent } from './components/folder-tree/folder-tree.component';
import { ContextmenuComponent } from './components/contextmenu/contextmenu.component';
import { FileViewListComponent } from './components/file-view-list/file-view-list.component';
import { NewFolderDialogComponent } from './modal/new-folder-dialog/new-folder-dialog.component';
import { RenameDialogComponent } from './modal/rename-dialog/rename-dialog.component';
import { ReactiveFormsModule } from '@angular/forms';
import { FolderPathViewerComponent } from './components/folder-path-viewer/folder-path-viewer.component';
import { MoveDialogComponent } from './modal/move-dialog/move-dialog.component';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  entryComponents: [
    NewFolderDialogComponent,
    RenameDialogComponent,
    MoveDialogComponent
  ],
  declarations: [
    FilemanagerComponent,
    FolderTreeComponent,
    FileViewListComponent,
    NewFolderDialogComponent,
    RenameDialogComponent,
    ContextmenuComponent,
    FolderPathViewerComponent,
    MoveDialogComponent
  ],
  imports: [
    CommonModule,
    LayoutModule,
    FilemanagerRoutingModule,
    ReactiveFormsModule,
    NgSelectModule
  ],
  providers: [
    TypeService,
    ObjectService
  ]
})
export class FilemanagerModule { }
