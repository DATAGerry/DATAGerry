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

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NewFolderDialogComponent } from './modal/new-folder-dialog/new-folder-dialog.component';
import { RenameDialogComponent } from './modal/rename-dialog/rename-dialog.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MoveDialogComponent } from './modal/move-dialog/move-dialog.component';
import { NgSelectModule } from '@ng-select/ng-select';
import { TypeService } from '../../../framework/services/type.service';
import { ObjectService} from '../../../framework/services/object.service';
import { MetadataInfoComponent } from './modal/metadata-info/metadata-info.component';

@NgModule({
    declarations: [

    ],
    imports: [
      CommonModule,
      ReactiveFormsModule,
      NgSelectModule,
      FormsModule
    ],
    exports: [
    ],
    providers: [
      TypeService,
      ObjectService
    ]
})
export class FileexplorerModule { }
