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

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { CmdbCategory, CmdbCategoryNode } from '../../../models/cmdb-category';
import { CmdbMode } from '../../../modes.enum';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { CategoryDeleteComponent } from '../../category-delete/category-delete.component';
import { NgbModalRef } from '@ng-bootstrap/ng-bootstrap/modal/modal-ref';
import { CategoryService } from '../../../services/category.service';
import { Router } from '@angular/router';
import { SidebarService } from '../../../../layout/services/sidebar.service';

@Component({
  selector: 'cmdb-category-node',
  templateUrl: './category-node.component.html',
  styleUrls: ['./category-node.component.scss']
})
export class CategoryNodeComponent implements OnDestroy {

  /**
   * Edit mode of tree
   */
  @Input() public mode: CmdbMode = CmdbMode.View;

  /**
   * Current node element
   */
  @Input() public node: CmdbCategoryNode;

  private deleteRef: NgbModalRef;

  public constructor(private deleteModal: NgbModal, private router: Router, private categoryService: CategoryService,
                     private sidebarService: SidebarService) {
  }

  public onDelete(category: CmdbCategory) {
    this.deleteRef = this.deleteModal.open(CategoryDeleteComponent);
    this.deleteRef.componentInstance.category = category;
    this.deleteRef.result.then((result) => {
      if (result === 'delete') {
        this.categoryService.deleteCategory(category.public_id).subscribe(() => {
          this.sidebarService.reload();
          this.router.navigate(['/', 'framework', 'category']);
        });
      }
    });
  }

  public ngOnDestroy(): void {
  }

}
