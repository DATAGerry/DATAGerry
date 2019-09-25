import { Component, OnInit } from '@angular/core';
import { FilePreview } from '../preview';
import { ImportService } from '../../../import.service';
import { ParserResponse } from '../preview.model';
import { HttpParams } from '@angular/common/http';

@Component({
  selector: 'cmdb-csv-preview',
  templateUrl: './csv-preview.component.html',
  styleUrls: ['./csv-preview.component.scss']
})
export class CsvPreviewComponent extends FilePreview implements OnInit {

  public parserResponse: ParserResponse;

  constructor(private importerService: ImportService) {
    super();
  }

  public ngOnInit(): void {

    const formData: FormData = new FormData();
    formData.append('file', this.file, this.file.name);
    this.importerService.postObjectParserFile(this.fileFormat, formData, this.config).subscribe((response: ParserResponse) => {
      this.parserResponse = response;
    });
  }

}
