import { Injectable } from "@angular/core";

import { CmdbType, CmdbTypeSection } from "src/app/framework/models/cmdb-type";
import { SectionIdentifierService } from "../../services/SectionIdentifierService.service";
import { ValidationService } from "../../services/validation.service";

@Injectable({
    providedIn: 'root'
})
export class SectionService {
    constructor(private validationService: ValidationService, private sectionIdentifierService: SectionIdentifierService) { }

    /**
     * Removes a section from the type instance and updates the fields and sections accordingly.
     * Handles both 'section' and 'ref-section' types.
     * @param typeInstance - The instance of the type containing the sections and fields.
     * @param sections - The array of sections from which an item will be removed.
     * @param item - The section item to be removed.
     * @param index - The index of the section to be removed.
     */
    removeSection(typeInstance: CmdbType, sections: Array<CmdbTypeSection>, item: CmdbTypeSection, index: number): void {
        if (index !== -1) {
            if (item.type === 'section') {
                const fields: Array<string> = typeInstance.render_meta.sections[index].fields;
                for (const field of fields) {
                    const fieldIdx = typeInstance.fields.map(x => x.name).indexOf(field['name']);
                    if (fieldIdx !== -1) {
                        typeInstance.fields.splice(fieldIdx, 1);
                    }
                }

                typeInstance.fields = [...typeInstance.fields];

            } else if (item.type === 'ref-section') {
                // Assuming removeRefSectionSelectionField is also moved to a service or utility
                this.removeRefSectionSelectionField(typeInstance, item);
            }

            sections.splice(index, 1);
            typeInstance.render_meta.sections.splice(index, 1);
            typeInstance.render_meta.sections = [...typeInstance.render_meta.sections];
        }
    }


    /**
     * Removes a reference section's field from the type instance fields.
     * Updates the fields list by removing the field associated with the specified reference section.
     * @param typeInstance - The instance of the type from which the field is removed.
     * @param refSection - The reference section whose field needs to be removed.
     */
    private removeRefSectionSelectionField(typeInstance: CmdbType, refSection: CmdbTypeSection): void {
        const index = typeInstance.fields.map(x => x.name).indexOf(`${refSection.name}-field`);
        typeInstance.fields.splice(index, 1);
        typeInstance.fields = [...typeInstance.fields];
    }

}
