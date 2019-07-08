/*
* dataGerry - OpenSource Enterprise CMDB
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

import { AfterContentInit, ChangeDetectorRef, Component, ViewChild } from '@angular/core';
import { BuilderComponent } from '../../../builder/builder.component';

@Component({
  selector: 'cmdb-type-fields-step',
  templateUrl: './type-fields-step.component.html',
  styleUrls: ['./type-fields-step.component.scss']
})
export class TypeFieldsStepComponent implements AfterContentInit {


  @ViewChild(BuilderComponent, {static: false})
  public typeBuilder: BuilderComponent;

  public constructor(private cdr: ChangeDetectorRef) {

  }

  public ngAfterContentInit(): void {
    this.cdr.detectChanges();
  }

}
