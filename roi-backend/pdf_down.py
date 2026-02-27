from fpdf import FPDF

class ROI_SOP(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'ROi Construction & Engineering LTD - Internal SOP', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 7, body)
        self.ln()

pdf = ROI_SOP()
pdf.add_page()

# Section 1: Philosophy
pdf.chapter_title('1. The ROi Philosophy')
pdf.chapter_body(
    "Zero Guesswork Policy: ROi Construction operates on a 100% precision mandate. No construction begins without rigorous pre-construction planning, soil assessment, and structural validation.\n"
    "The 'Unseen Quality' Rule: We prioritize structural elements that are eventually hidden (foundations, rebar, compaction) because they determine the lifespan of the building.\n"
    "Mission: To build structures that grow in worth, comfort, and design through meticulous engineering."
)

# Section 2: Technical Standards
pdf.chapter_title('2. Technical Service Standards')
pdf.chapter_body(
    "Pre-Construction Planning: Includes site analysis, soil testing, and flawless execution strategies to eliminate financial risks for clients.\n"
    "Structural Engineering: Specialized expertise in rebar placement, column casting, and slab integrity.\n"
    "Lean Project Management: Utilizing 'Whole Life Costing' to ensure that the initial investment results in long-term savings and a guaranteed ROI."
)

# Section 3: QA/QC
pdf.chapter_title('3. Quality Assurance & Quality Control (QA/QC)')
pdf.chapter_body(
    "Materials: Only certified, high-grade materials are permitted on ROi sites.\n"
    "Compaction & Soil Testing: Skipping soil testing or rushing compaction is strictly prohibited as it creates structural risks and financial losses.\n"
    "Verification: Every beam, block, and brick must represent a promise of safety, honesty, and precision."
)

# Section 4: Contact
pdf.chapter_title('4. Contact & Operations')
pdf.chapter_body(
    "Primary Region: Nigeria, with active operations in Lagos and surrounding areas.\n"
    "Official Correspondence: All technical inquiries should be directed to roiconstructionng@gmail.com."
)

pdf.output('ROi_SOP.pdf')
print("Successfully created ROi_SOP.pdf")