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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, Input } from '@angular/core';
import { CmdbCategoryTree } from '../../../models/cmdb-category';
import { DropEffect } from 'ngx-drag-drop';
import { CmdbMode } from '../../../modes.enum';

@Component({
  selector: 'cmdb-category-tree',
  templateUrl: './category-tree.component.html',
  styleUrls: ['./category-tree.component.scss']
})
export class CategoryTreeComponent {

  /**
   * Edit mode of tree
   */
  @Input() public mode: CmdbMode = CmdbMode.View;

  /**
   * Root element of the category tree
   */
  @Input() public tree: CmdbCategoryTree;

  public effect: DropEffect = 'move';


}
