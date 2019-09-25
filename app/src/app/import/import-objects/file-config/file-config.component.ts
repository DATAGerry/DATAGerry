import {
  Component, ComponentFactory,
  ComponentFactoryResolver,
  ComponentRef,
  Input,
  OnChanges,
  OnInit,
  SimpleChanges,
  ViewChild,
  ViewContainerRef
} from '@angular/core';
import { CsvConfigComponent } from './csv-config/csv-config.component';
import { JsonConfigComponent } from './json-config/json-config.component';
import { FileConfig } from './file-config';

export const configComponents: { [type: string]: any } = {
  json: JsonConfigComponent,
  csv: CsvConfigComponent
};

@Component({
  selector: 'cmdb-file-config',
  templateUrl: './file-config.component.html',
  styleUrls: ['./file-config.component.scss']
})
export class FileConfigComponent extends FileConfig implements OnInit, OnChanges {

  @ViewChild('fileConfig', { read: ViewContainerRef, static: true }) fileConfig;
  @Input() fileFormat: string = 'json';

  private component: any;
  public componentRef: ComponentRef<any>;
  private currentFactory: ComponentFactory<any>;

  constructor(private resolver: ComponentFactoryResolver) {
    super();
  }

  public ngOnInit(): void {
    this.fileConfig.clear();
  }

  public ngOnChanges(changes: SimpleChanges): void {
    if (changes.fileFormat !== undefined && changes.fileFormat.currentValue !== undefined
      && changes.fileFormat.firstChange === false) {
      this.fileConfig.clear();
      this.component = configComponents[this.fileFormat];
      this.currentFactory = this.resolver.resolveComponentFactory(this.component);
    }
    if (changes.defaultParserConfig !== undefined && changes.defaultParserConfig.currentValue !== undefined
      && changes.defaultParserConfig.firstChange === false) {
      this.componentRef = this.fileConfig.createComponent(this.currentFactory);
      this.componentRef.instance.configForm = this.configForm;
      this.componentRef.instance.defaultParserConfig = this.defaultParserConfig;
    }
  }

}
