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

import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { CmdbCategory, CmdbCategoryNode } from '../../../models/cmdb-category';
import { CmdbMode } from '../../../modes.enum';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { NgbModalRef } from '@ng-bootstrap/ng-bootstrap/modal/modal-ref';
import { CategoryService } from '../../../services/category.service';
import { Router } from '@angular/router';
import { DeleteCategoryModalComponent } from '../modals/delete-category-modal/delete-category-modal.component';

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

  /**
   * Node change emitter
   */
  @Output() public change: EventEmitter<{ type: string, value: any }>;

  private deleteRef: NgbModalRef;

  public constructor(private deleteModal: NgbModal, private router: Router, private categoryService: CategoryService) {
    this.change = new EventEmitter<{ type: string, value: any }>();
  }

  public onDelete(category: CmdbCategory) {
    this.deleteRef = this.deleteModal.open(DeleteCategoryModalComponent);
    this.deleteRef.componentInstance.category = category;
    this.deleteRef.result.then((result) => {
      if (result === 'delete') {
        this.categoryService.deleteCategory(category.public_id).subscribe((id: number) => {
          this.change.emit({ type: 'delete', value: 'id' });
        });
      }
    });
  }

  public ngOnDestroy(): void {
  }

}
