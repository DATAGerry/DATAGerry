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

import {
  Component, ComponentFactory,
  ComponentFactoryResolver,
  ComponentRef, EventEmitter,
  Input,
  OnChanges, OnDestroy,
  OnInit, Output,
  SimpleChanges,
  ViewChild,
  ViewContainerRef
} from '@angular/core';
import { CsvConfigComponent } from './csv-config/csv-config.component';
import { JsonConfigComponent } from './json-config/json-config.component';
import { FileConfig } from './file-config';
import { ImportService } from '../../import.service';
import { Subscription } from 'rxjs';

export const configComponents: { [type: string]: any } = {
  json: JsonConfigComponent,
  csv: CsvConfigComponent
};

@Component({
  selector: 'cmdb-file-config',
  templateUrl: './file-config.component.html',
  styleUrls: ['./file-config.component.scss']
})
export class FileConfigComponent extends FileConfig implements OnInit, OnChanges, OnDestroy {

  @ViewChild('fileConfig', { read: ViewContainerRef, static: true }) fileConfig;
  @Input() fileFormat: string = 'json';

  @Output() public configChange: EventEmitter<any>;
  private configChangeSubscription: Subscription;

  private component: any;
  public componentRef: ComponentRef<any>;
  private currentFactory: ComponentFactory<any>;

  constructor(private resolver: ComponentFactoryResolver, private importService: ImportService) {
    super();
    this.configChange = new EventEmitter<any>();
    this.configChangeSubscription = new Subscription();
  }

  public ngOnInit(): void {
    this.configForm.valueChanges.subscribe(() => {
      this.configChange.emit(this.configForm.getRawValue());
    });
    this.fileConfig.clear();
  }

  public ngOnChanges(changes: SimpleChanges): void {
    if (changes.fileFormat !== undefined && (changes.fileFormat.currentValue !== undefined || changes.fileFormat.currentValue !== '')
      && changes.fileFormat.firstChange === false) {
      this.fileConfig.clear();
      this.component = configComponents[this.fileFormat];
      this.currentFactory = this.resolver.resolveComponentFactory(this.component);

      this.importService.getObjectParserDefaultConfig(this.fileFormat).subscribe(defaultParserConfig => {
        this.defaultParserConfig = defaultParserConfig;
        this.componentRef = this.fileConfig.createComponent(this.currentFactory);
        this.componentRef.instance.configForm = this.configForm;
        this.componentRef.instance.defaultParserConfig = this.defaultParserConfig;
      });
    }
  }

  public ngOnDestroy(): void {
    this.configChangeSubscription.unsubscribe();
  }
}
