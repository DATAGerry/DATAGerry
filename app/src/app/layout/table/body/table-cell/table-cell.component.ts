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
import {
  Component,
  ComponentFactoryResolver, HostBinding,
  Input,
  OnInit,
  ViewChild,
  ViewContainerRef
} from '@angular/core';
import { Column } from '../../table.types';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'td[table-cell]',
  templateUrl: './table-cell.component.html',
  styleUrls: ['./table-cell.component.scss']
})
export class TableCellComponent<T> implements OnInit {

  @HostBinding('class.hidden') private hidden: boolean = false;

  @Input() rowIndex: number;

  public data: any;
  public item: T;


  public column: Column;

  @Input('column')
  public set Column(col: Column) {
    this.column = col;
    this.hidden = this.column.hidden;
  }

  @Input('item')
  public set Item(item: T) {
    this.item = item;
    if (this.column.data) {
      this.data = TableCellComponent.resolve(this.column.data, this.item);
    }
  }

  /**
   * Resolves a given objects path to a value.
   * @param path to the property
   * @param obj resolvable object
   * @param separator ident
   */
  static resolve(path, obj, separator = '.') {
    const properties = Array.isArray(path) ? path : path.split(separator);
    return properties.reduce((prev, curr) => prev && prev[curr], obj);
  }

  constructor(private resolver: ComponentFactoryResolver) {
  }

  public ngOnInit(): void {

  }

}
