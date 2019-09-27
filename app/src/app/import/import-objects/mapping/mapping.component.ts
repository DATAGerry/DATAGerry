import { Component, Input, OnChanges, OnDestroy, OnInit, SimpleChanges } from '@angular/core';
import { Subject } from 'rxjs';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { FilePreview } from './preview';
import { ParserResult } from './preview.model';
import { ImportService } from '../../import.service';

@Component({
  selector: 'cmdb-preview',
  templateUrl: './preview.component.html',
  styleUrls: ['./preview.component.scss']
})
export class PreviewComponent extends FilePreview implements OnInit, OnChanges, OnDestroy {

  public parserResponse: ParserResult;
  public header: boolean = false;
  public columns: [];

  public config: any;
  @Input() file: File;
  @Input() fileFormat: string;
  @Input() typeInstance: CmdbType;
  @Input() previewTrigger: Subject<any>;

  constructor(private importerService: ImportService) {
    super();
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
      });
    });
  }

  public ngOnChanges(changes: SimpleChanges): void {

    if

  }

  public ngOnDestroy(): void {
    this.previewTrigger.unsubscribe();
  }

}
