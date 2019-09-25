import {
  Component,
  ComponentFactory,
  ComponentFactoryResolver,
  ComponentRef,
  Input,
  OnDestroy,
  OnInit,
  ViewChild,
  ViewContainerRef
} from '@angular/core';
import { Subject } from 'rxjs';
import { CsvPreviewComponent } from './csv-preview/csv-preview.component';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { FilePreview } from './preview';

export const previewComponents: { [type: string]: any } = {
  csv: CsvPreviewComponent,
};


@Component({
  selector: 'cmdb-preview',
  templateUrl: './preview.component.html',
  styleUrls: ['./preview.component.scss']
})
export class PreviewComponent extends FilePreview implements OnInit, OnDestroy {

  @ViewChild('previewContainer', { read: ViewContainerRef, static: true }) previewContainer;

  public config: any;

  @Input() file: File;
  @Input() fileFormat: string;
  @Input() typeInstance: CmdbType;
  @Input() previewTrigger: Subject<any>;

  private component: any;
  private componentRef: ComponentRef<any>;
  private currentFactory: ComponentFactory<any>;

  constructor(private resolver: ComponentFactoryResolver) {
    super();
  }

  public ngOnInit(): void {
    this.previewTrigger.subscribe((config) => {
      this.config = config;
      this.previewContainer.clear();
      this.component = previewComponents[this.fileFormat];
      this.currentFactory = this.resolver.resolveComponentFactory(this.component);
      this.componentRef = this.previewContainer.createComponent(this.currentFactory);
      this.componentRef.instance.config = this.config;
      this.componentRef.instance.file = this.file;
      this.componentRef.instance.fileFormat = this.fileFormat;
      this.componentRef.instance.typeInstance = this.typeInstance;
    });
  }

  public ngOnDestroy(): void {
    this.previewTrigger.unsubscribe();
  }

}
