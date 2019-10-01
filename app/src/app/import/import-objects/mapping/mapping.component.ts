import { Component, Input, OnChanges, OnDestroy, OnInit, SimpleChanges } from '@angular/core';
import { Subject } from 'rxjs';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { ParserResult } from './mapping.model';
import { ImportService } from '../../import.service';
import { DndDropEvent } from 'ngx-drag-drop';


@Component({
  selector: 'cmdb-mapping',
  templateUrl: './mapping.component.html',
  styleUrls: ['./mapping.component.scss']
})
export class MappingComponent implements OnInit, OnChanges, OnDestroy {

  @Input() file: File;
  @Input() fileFormat: string;
  @Input() typeInstance: CmdbType;
  @Input() previewTrigger: Subject<any>;

  public parserResponse: ParserResult;
  public header: boolean = false;
  public columns: [];
  public publicID = {
    label: 'public_id'
  };
  public active = {
    label: 'active'
  };
  public fieldList: any[];
  public mapping: { [rowIdx: number]: any };
  public config: any;

  constructor(private importerService: ImportService) {
  }

  public ngOnInit(): void {
    this.previewTrigger.subscribe(config => {
      this.config = config;
      const formData: FormData = new FormData();
      formData.append('file', this.file, this.file.name);
      this.importerService.postObjectParserFile(this.fileFormat, formData, this.config).subscribe((response: ParserResult) => {
          this.parserResponse = response;
          this.header = this.parserResponse.header !== [];
          if (this.header) {
            this.columns = this.parserResponse.header;
          } else {
            this.columns = this.parserResponse.lines[0];
          }
        },
        (error) => {
          console.error(error);
        },
        () => {

        });
    });
  }

  public ngOnChanges(changes: SimpleChanges): void {
    if (changes.typeInstance !== undefined && !changes.typeInstance.firstChange && changes.typeInstance.currentValue !== undefined) {
      this.mapping = {};
      this.fieldList = this.typeInstance.fields;
    }
  }

  public ngOnDestroy(): void {
    this.previewTrigger.unsubscribe();
  }

  public onDragged(item: any) {
    const index = this.fieldList.indexOf(item);
    this.fieldList.splice(index, 1);
  }

  public onDrop(event: DndDropEvent, rowIdx: number) {
    this.mapping[rowIdx] = event.data;
  }

}
