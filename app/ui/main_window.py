"""
Main window for the Quote Poster Generator application.
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSplitter, QFileDialog, QMessageBox, QComboBox, QSpinBox,
    QColorDialog, QTextEdit, QFrame, QGroupBox,
    QListWidget, QListWidgetItem, QDialog, QDialogButtonBox, QSlider
)
from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal, QEventLoop
from PyQt6.QtGui import QPixmap, QColor, QFont, QPainter, QImage, QIcon
import os
from pathlib import Path

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize state before UI
        self.current_background = None
        self.current_font = QFont("Arial", 24)
        self.text_color = QColor("white")
        self.alignment = Qt.AlignmentFlag.AlignCenter
        self.text_x_position = 0  # Range: -100 to 100
        self.text_y_position = 0  # Range: -100 to 100
        
        # Window properties
        self.setWindowTitle("Quote Poster Generator")
        self.setMinimumSize(1000, 700)
        
        # Initialize UI
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Controls
        control_panel = self.create_control_panel()
        splitter.addWidget(control_panel)
        
        # Right panel - Preview
        preview_panel = self.create_preview_panel()
        splitter.addWidget(preview_panel)
        
        # Set initial sizes
        splitter.setSizes([300, 700])
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_control_panel(self) -> QWidget:
        """Create the control panel with all the controls."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Background section
        bg_group = QGroupBox("Background")
        bg_layout = QVBoxLayout(bg_group)
        
        # Background selection buttons
        btn_bg_collection = QPushButton("From Collection")
        btn_bg_collection.clicked.connect(self.load_background_from_collection)
        bg_layout.addWidget(btn_bg_collection)
        
        btn_bg_custom = QPushButton("Load Custom Background")
        btn_bg_custom.clicked.connect(self.load_custom_background)
        bg_layout.addWidget(btn_bg_custom)
        
        btn_bg_generate = QPushButton("Generate with AI")
        btn_bg_generate.clicked.connect(self.generate_background_ai)
        bg_layout.addWidget(btn_bg_generate)
        
        layout.addWidget(bg_group)
        
        # Text section
        text_group = QGroupBox("Quote Text")
        text_layout = QVBoxLayout(text_group)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter your quote here...")
        self.text_edit.textChanged.connect(self.update_preview)
        text_layout.addWidget(self.text_edit)
        
        # Text controls
        controls_layout = QVBoxLayout()
        
        # Font controls group
        font_group = QGroupBox("Font")
        font_group_layout = QVBoxLayout(font_group)
        
        # Font family
        font_layout = QHBoxLayout()
        font_label = QLabel("Font:")
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"])
        self.font_combo.setCurrentText("Arial")
        self.font_combo.currentTextChanged.connect(self.change_font_family)
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_combo)
        font_group_layout.addLayout(font_layout)
        
        # Font size
        size_layout = QHBoxLayout()
        size_label = QLabel("Size:")
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 144)
        self.size_spin.setValue(24)
        self.size_spin.valueChanged.connect(self.change_font_size)
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_spin)
        font_group_layout.addLayout(size_layout)
        
        # Text color
        color_btn = QPushButton("Text Color")
        color_btn.clicked.connect(self.choose_text_color)
        font_group_layout.addWidget(color_btn)
        
        # Text alignment
        align_layout = QHBoxLayout()
        align_label = QLabel("Alignment:")
        self.align_combo = QComboBox()
        self.align_combo.addItem("Left", Qt.AlignmentFlag.AlignLeft)
        self.align_combo.addItem("Center", Qt.AlignmentFlag.AlignCenter)
        self.align_combo.addItem("Right", Qt.AlignmentFlag.AlignRight)
        self.align_combo.setCurrentIndex(1)  # Default to Center
        self.align_combo.currentIndexChanged.connect(self.change_text_alignment)
        align_layout.addWidget(align_label)
        align_layout.addWidget(self.align_combo)
        font_group_layout.addLayout(align_layout)
        
        # Add font group to controls
        controls_layout.addWidget(font_group)
        
        # Position controls group
        pos_group = QGroupBox("Text Position")
        pos_layout = QVBoxLayout(pos_group)
        
        # Horizontal position slider
        h_layout = QVBoxLayout()
        h_label = QLabel("Horizontal Position")
        self.h_slider = QSlider(Qt.Orientation.Horizontal)
        self.h_slider.setRange(-100, 100)
        self.h_slider.setValue(0)
        self.h_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.h_slider.setTickInterval(25)
        self.h_slider.valueChanged.connect(self.update_text_position)
        h_layout.addWidget(h_label)
        h_layout.addWidget(self.h_slider)
        pos_layout.addLayout(h_layout)
        
        # Vertical position slider
        v_layout = QVBoxLayout()
        v_label = QLabel("Vertical Position")
        self.v_slider = QSlider(Qt.Orientation.Horizontal)
        self.v_slider.setRange(-100, 100)
        self.v_slider.setValue(0)
        self.v_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.v_slider.setTickInterval(25)
        self.v_slider.valueChanged.connect(self.update_text_position)
        v_layout.addWidget(v_label)
        v_layout.addWidget(self.v_slider)
        pos_layout.addLayout(v_layout)
        
        # Add position group to controls
        controls_layout.addWidget(pos_group)
        
        # Add controls to text layout
        text_layout.addLayout(controls_layout)
        
        layout.addWidget(text_group)
        
        # Export button
        btn_export = QPushButton("Export Poster")
        btn_export.clicked.connect(self.export_poster)
        layout.addWidget(btn_export)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        return panel
    
    def create_preview_panel(self) -> QWidget:
        """Create the preview panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Preview label
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(640, 480)
        self.preview_label.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.preview_label)
        
        # Set default preview
        self.update_preview()
        
        return panel
    
    def load_background_from_collection(self):
        """Load a background from the collection with a selection dialog."""
        try:
            # Get the absolute path to the backgrounds directory
            # The backgrounds are in the quote_poster_generator/assets/backgrounds directory
            try:
                current_file = Path(__file__).resolve()
                bg_dir = current_file.parent.parent.parent / "assets" / "backgrounds"
                bg_dir = bg_dir.resolve()
            except Exception as e:
                error_msg = f"Error resolving paths: {str(e)}"
                print(error_msg)
                QMessageBox.critical(self, "Path Error", error_msg)
                return
            
            # Debug output
            print(f"Looking for backgrounds in: {bg_dir}")
            print(f"Directory exists: {bg_dir.exists()}")
            
            if not bg_dir.exists():
                error_msg = (
                    f"Backgrounds directory not found at: {bg_dir}\n"
                    "Please make sure the 'assets/backgrounds' directory exists and contains image files."
                )
                print(error_msg)
                QMessageBox.critical(self, "Directory Not Found", error_msg)
                return
            
            # Get all image files in the directory (case-insensitive)
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
            image_files = []
            
            for ext in image_extensions:
                # Search for both lowercase and uppercase extensions
                image_files.extend(bg_dir.glob(f'*{ext}'))
                if ext != ext.upper():
                    image_files.extend(bg_dir.glob(f'*{ext.upper()}'))
            
            # Remove duplicates and sort
            image_files = sorted(list(set(image_files)))
            
            if not image_files:
                error_msg = (
                    f"No image files found in: {bg_dir}\n"
                    f"Supported formats: {', '.join(image_extensions)}\n"
                    "Please add some image files to this directory."
                )
                print(error_msg)
                QMessageBox.warning(self, "No Images Found", error_msg)
                return
            
            if not image_files:
                QMessageBox.warning(
                    self, 
                    "No Backgrounds", 
                    "No background images found in the collection.\n\n"
                    "Please add some images to the 'assets/backgrounds' directory."
                )
                return
                
            # Create a dialog to select from available backgrounds
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QDialogButtonBox
            
            class BackgroundDialog(QDialog):
                def __init__(self, image_files, parent=None):
                    super().__init__(parent)
                    self.setWindowTitle("Select Background")
                    self.setMinimumSize(600, 400)
                    
                    layout = QVBoxLayout(self)
                    
                    # Create list widget for image selection
                    self.list_widget = QListWidget()
                    self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
                    self.list_widget.setIconSize(QSize(150, 150))
                    self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
                    self.list_widget.setSpacing(10)
                    
                    # Add images to the list
                    for img_file in image_files:
                        pixmap = QPixmap(str(img_file))
                        if not pixmap.isNull():
                            # Create a thumbnail
                            thumb = pixmap.scaled(
                                150, 150, 
                                Qt.AspectRatioMode.KeepAspectRatio,
                                Qt.TransformationMode.SmoothTransformation
                            )
                            item = QListWidgetItem(img_file.name)
                            item.setIcon(QIcon(thumb))
                            item.setData(Qt.ItemDataRole.UserRole, img_file)
                            item.setToolTip(img_file.name)
                            self.list_widget.addItem(item)
                    
                    # Select the first item by default
                    if self.list_widget.count() > 0:
                        self.list_widget.setCurrentRow(0)
                    
                    # Add buttons
                    button_box = QDialogButtonBox(
                        QDialogButtonBox.StandardButton.Ok | 
                        QDialogButtonBox.StandardButton.Cancel
                    )
                    button_box.accepted.connect(self.accept)
                    button_box.rejected.connect(self.reject)
                    
                    # Add widgets to layout
                    layout.addWidget(self.list_widget)
                    layout.addWidget(button_box)
                
                def selected_file(self):
                    """Get the selected file path."""
                    items = self.list_widget.selectedItems()
                    if items:
                        return items[0].data(Qt.ItemDataRole.UserRole)
                    return None
            
            # Show the dialog
            dialog = BackgroundDialog(image_files, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                selected_file = dialog.selected_file()
                if selected_file:
                    self.current_background = QPixmap(str(selected_file))
                    if not self.current_background.isNull():
                        self.update_preview()
                        self.statusBar().showMessage(f"Loaded: {selected_file.name}")
                    else:
                        QMessageBox.warning(self, "Error", f"Failed to load image: {selected_file.name}")
                        
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error", 
                f"Failed to load background: {str(e)}\n\n"
                f"Please make sure the 'assets/backgrounds' directory exists and contains valid images."
            )
    
    def load_custom_background(self):
        """Load a custom background image."""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Background Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_name:
            self.current_background = QPixmap(file_name)
            self.update_preview()
    
    def generate_background_ai(self):
        """Generate a background using AI."""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox, QProgressDialog
        from PyQt6.QtCore import Qt
        
        # Show input dialog for prompt
        prompt, ok = QInputDialog.getMultiLineText(
            self, 
            "Generate AI Background",
            "Describe the background you want to generate:",
            text="A beautiful landscape with mountains and a lake, digital art"
        )
        
        if not ok or not prompt.strip():
            return
            
        # Create progress dialog
        progress = QProgressDialog(
            "Generating AI background...",
            "Cancel", 0, 100, self
        )
        progress.setWindowTitle("Please Wait")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        
        # Initialize AI generator
        from app.core.ai_generator import AIGenerator, AIGenerationResult
        
        # Create a worker thread for the generation
        class GenerationThread(QThread):
            finished_signal = pyqtSignal(AIGenerationResult)
            progress_signal = pyqtSignal(int)
            
            def __init__(self, prompt, size):
                super().__init__()
                self.prompt = prompt
                self.size = size
                self.ai_gen = AIGenerator()
                self._is_cancelled = False
            
            def run(self):
                try:
                    if not self.ai_gen.is_configured():
                        self.finished_signal.emit(AIGenerationResult(
                            success=False,
                            error="AI generation is not properly configured.\n"
                                 "Please set up your API keys in the .env file."
                        ))
                        return
                    
                    # Connect progress signals
                    self.ai_gen.progress_updated.connect(self.progress_signal.emit)
                    
                    # Create an event loop to wait for the generation to complete
                    loop = QEventLoop()
                    self.ai_gen.generation_finished.connect(loop.quit)
                    
                    # Start generation
                    self.ai_gen.generate_background(self.prompt, self.size)
                    
                    # Show progress dialog
                    self.progress_signal.emit(10)
                    
                    # Wait for generation to complete
                    loop.exec()
                    
                except Exception as e:
                    self.finished_signal.emit(AIGenerationResult(
                        success=False,
                        error=f"Error during generation: {str(e)}"
                    ))
        
        # Create and start the worker thread
        self.generation_thread = GenerationThread(prompt, (1024, 1024))
        
        # Connect signals
        def on_progress_updated(value):
            progress.setValue(value)
            
        def on_generation_finished(result):
            progress.close()
            
            if result.success and result.image:
                self.current_background = result.image
                self.update_preview()
                self.statusBar().showMessage("AI background generated successfully!")
            else:
                QMessageBox.warning(
                    self,
                    "Generation Failed",
                    f"Failed to generate background: {result.error or 'Unknown error'}\n\n"
                    "Please check your API key and internet connection."
                )
        
        # Connect signals
        self.generation_thread.finished_signal.connect(on_generation_finished)
        self.generation_thread.progress_signal.connect(on_progress_updated)
        
        # Cancel handling
        progress.canceled.connect(self.generation_thread.terminate)
        
        # Start the generation
        self.generation_thread.start()
    
    def change_font_family(self, font_family):
        """Change the font family."""
        self.current_font.setFamily(font_family)
        self.update_preview()
    
    def change_font_size(self, size):
        """Change the font size."""
        self.current_font.setPointSize(size)
        self.update_preview()
    
    def choose_text_color(self):
        """Open a color dialog to choose text color."""
        color = QColorDialog.getColor(self.text_color, self, "Choose Text Color")
        if color.isValid():
            self.text_color = color
            self.update_preview()
            
    def change_text_alignment(self, index):
        """Change the text alignment based on combo box selection."""
        alignment = self.align_combo.currentData()
        if alignment is not None:
            self.alignment = alignment
            self.update_preview()
    
    def set_alignment(self, alignment):
        """Set the text alignment."""
        self.alignment = alignment
        self.update_preview()
    
    def update_text_position(self):
        """Update text position based on slider values and refresh preview."""
        if hasattr(self, 'h_slider') and hasattr(self, 'v_slider'):
            self.text_x_position = self.h_slider.value()
            self.text_y_position = self.v_slider.value()
            self.update_preview()

    def update_preview(self):
        """Update the preview with the current state."""
        if not hasattr(self, 'preview_label') or not hasattr(self, 'current_background') or not self.current_background:
            return
            
        try:
            # Create a blank pixmap with the same size as the label
            preview_size = self.preview_label.size()
            if preview_size.width() <= 0 or preview_size.height() <= 0:
                return
                
            # Create a pixmap to draw on
            pixmap = QPixmap(preview_size)
            pixmap.fill(Qt.GlobalColor.white)
            
            # Draw the background
            scaled_bg = self.current_background.scaled(
                preview_size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            
            # Center the background
            x = (preview_size.width() - scaled_bg.width()) // 2
            y = (preview_size.height() - scaled_bg.height()) // 2
            
            # Create a painter for the pixmap
            painter = QPainter(pixmap)
            painter.drawPixmap(x, y, scaled_bg)
            
            # Draw the text if available
            if hasattr(self, 'text_edit') and hasattr(self, 'current_font') and hasattr(self, 'text_color'):
                text = self.text_edit.toPlainText()
                if text:
                    # Configure text rendering
                    painter.setFont(self.current_font)
                    painter.setPen(self.text_color)
                    
                    # Set up text rectangle with margins
                    margin = 40
                    text_rect = pixmap.rect().adjusted(margin, margin, -margin, -margin)
                    
                    # Calculate position offset based on slider values (-100 to 100)
                    text_width = text_rect.width()
                    text_height = text_rect.height()
                    
                    # Calculate position offset based on slider values
                    x_offset = int((self.text_x_position / 100.0) * (text_width / 2))
                    y_offset = int((self.text_y_position / 100.0) * (text_height / 2))
                    
                    # Adjust text rectangle based on horizontal position
                    if self.alignment & Qt.AlignmentFlag.AlignLeft:
                        text_rect.adjust(x_offset, 0, x_offset, 0)
                    elif self.alignment & Qt.AlignmentFlag.AlignRight:
                        text_rect.adjust(-x_offset, 0, -x_offset, 0)
                    else:  # Center alignment (default)
                        text_rect.adjust(x_offset, 0, x_offset, 0)
                    
                    # Apply vertical offset
                    text_rect.adjust(0, y_offset, 0, y_offset)
                    
                    # Draw the text with word wrap and alignment
                    painter.drawText(
                        text_rect,
                        self.alignment | Qt.TextFlag.TextWordWrap,
                        text
                    )
                    
        except Exception as e:
            print(f"Error updating preview: {e}")
            return
            
        finally:
            if 'painter' in locals() and painter.isActive():
                painter.end()
        
        # Update the preview
        self.preview_label.setPixmap(pixmap)
    
    def export_poster(self):
        """Export the current poster as an image file."""
        try:
            # Check if there's a background loaded
            if not hasattr(self, 'current_background') or not self.current_background or self.current_background.isNull():
                QMessageBox.warning(self, "No Background", "Please load or generate a background first.")
                return
                
            # Get the text to include in the filename
            text = self.text_edit.toPlainText() if hasattr(self, 'text_edit') else "poster"
            safe_text = "".join([c if c.isalnum() or c in ' _-' else '_' for c in text])
            default_name = f"{safe_text[:30]}_poster.png"
            
            # Open file dialog to choose save location
            file_name, selected_filter = QFileDialog.getSaveFileName(
                self,
                "Save Poster As",
                str(Path.home() / "Pictures" / default_name),
                "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;All Files (*)"
            )
            
            if not file_name:
                return
                
            # Determine the file format from the selected filter or file extension
            if selected_filter.startswith("PNG") or file_name.lower().endswith('.png'):
                if not file_name.lower().endswith('.png'):
                    file_name += '.png'
                format = 'PNG'
            else:  # Default to JPEG
                if not file_name.lower().endswith(('.jpg', '.jpeg')):
                    file_name += '.jpg'
                format = 'JPEG'
            
            # Get the current preview pixmap
            pixmap = self.preview_label.pixmap()
            if not pixmap or pixmap.isNull():
                raise ValueError("No preview available to save")
            
            # Save the pixmap to file
            success = pixmap.save(file_name, format, quality=95 if format == 'JPEG' else -1)
            
            if success:
                self.statusBar().showMessage(f"Poster saved to {file_name}", 5000)
                QMessageBox.information(self, "Success", f"Poster saved successfully to:\n{file_name}")
            else:
                raise Exception("Failed to save image file")
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Failed to save poster: {str(e)}"
            )
