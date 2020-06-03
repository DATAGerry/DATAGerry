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
import { Component, OnChanges, OnDestroy, OnInit, SimpleChanges, ViewChild } from '@angular/core';
import { Subscription } from 'rxjs';
import { CmdbCategoryNode, CmdbCategoryTree } from '../models/cmdb-category';
import { CategoryService } from '../services/category.service';
import { ITreeOptions, TreeComponent, TreeNode } from 'angular-tree-component';

@Component({
  selector: 'cmdb-category',
  templateUrl: './category.component.html',
  styleUrls: ['./category.component.scss']
})
export class CategoryComponent implements OnInit, OnDestroy {


  constructor(private categoryService: CategoryService) {
    this.categoryTreeSubscription = new Subscription();
  }

  private categoryTreeSubscription: Subscription;
  public categoryTree: CmdbCategoryTree;

  public nodes: any[] = [];
  @ViewChild(TreeComponent, { static: false }) tree: TreeComponent;

  public treeOptions: ITreeOptions = {
    displayField: 'name',
    childrenField: 'children',
    allowDrag: (node) => {
      return true;
    },
    allowDrop: (node) => {
      return true;
    },
    allowDragoverStyling: true
  };

  static convertNode(node: any): any {
    const children = [];
    for (const child of node.children) {
      children.push(CategoryComponent.convertNode(child));
    }
    return {
      data: node,
      name: node.category.label,
      id: node.category.public_id,
      children
    };
  }

  public ngOnInit(): void {
    this.categoryTreeSubscription = this.categoryService.getCategoryTree().subscribe((categoryTree: CmdbCategoryTree) => {
      this.categoryTree = categoryTree;
      for (const categoryNode of this.categoryTree) {
        const node = CategoryComponent.convertNode(categoryNode);
        this.nodes.push(node);
      }
      this.tree.treeModel.update();
    });
  }


  public ngOnDestroy(): void {
    this.categoryTreeSubscription.unsubscribe();
  }


}
