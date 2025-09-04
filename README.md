# 📊 AI File Insights Extractor

A Streamlit application that uploads user-provided files to OpenAI's API to extract context-appropriate insights for the given data.

## 🚀 Features

- **Multi-file Upload**: Support for various file types (TXT, CSV, JSON, PDF, DOCX, XLSX, MD)
- **OpenAI Integration**: Uses OpenAI's GPT models for intelligent analysis
- **Multiple Analysis Types**: 
  - General Insights
  - Data Analysis
  - Document Summary
  - Custom Analysis
- **Interactive UI**: Clean, modern Streamlit interface
- **Progress Tracking**: Real-time progress indicators
- **Download Results**: Export insights as text files
- **Token Usage Tracking**: Monitor API usage

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- Required packages (see requirements.txt)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your OpenAI API key**:
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new API key
   - Keep it secure and never commit it to version control

## 🚀 Usage

1. **Run the application**:
   ```bash
   streamlit run app.py
   ```

2. **Configure the application**:
   - Enter your OpenAI API key in the sidebar
   - Select your preferred model (GPT-4o recommended for best results)
   - Choose the analysis type

3. **Upload and analyze files**:
   - Upload one or more files using the file uploader
   - Click "Analyze Files" to start the analysis
   - View results in the expandable sections
   - Download individual insights or all results

## 📁 Supported File Types

| File Type | Extension | Description |
|-----------|-----------|-------------|
| Text | `.txt`, `.md` | Plain text and Markdown files |
| CSV | `.csv` | Comma-separated values with data preview |
| JSON | `.json` | JSON data with structure analysis |
| Excel | `.xlsx` | Excel spreadsheets with data summary |
| PDF | `.pdf` | PDF documents (text extraction) |
| Word | `.docx` | Microsoft Word documents |

## 🎯 Analysis Types

### General Insights
- Main themes and patterns identification
- Important data points extraction
- Areas of interest or concern
- Key takeaways summary
- Actionable recommendations

### Data Analysis
- Data structure and quality assessment
- Statistical summaries and trends
- Anomaly detection
- Correlation analysis
- Business insights

### Document Summary
- Executive summary creation
- Key points extraction
- Important facts and figures
- Conclusions and recommendations
- Action items identification

### Custom Analysis
- User-defined analysis prompts
- Tailored insights extraction
- Specific question answering
- Domain-specific analysis

## ⚙️ Configuration Options

- **Model Selection**: Choose from GPT-4o, GPT-4o-mini, GPT-4-turbo, or GPT-3.5-turbo
- **Analysis Type**: Select from predefined analysis types or create custom prompts
- **File Upload**: Support for multiple files and various formats
- **Token Tracking**: Monitor API usage and costs

## 🔒 Security Notes

- Never commit your OpenAI API key to version control
- Use environment variables for production deployments
- Be mindful of file content sensitivity when uploading
- Monitor API usage to control costs

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your OpenAI API key is valid and has sufficient credits
2. **File Upload Error**: Check that file types are supported and files aren't corrupted
3. **Memory Issues**: Large files may cause memory issues; consider splitting them
4. **Rate Limits**: OpenAI has rate limits; wait and retry if you hit them

### Error Messages

- `Error reading file`: File format not supported or corrupted
- `API Error`: Check your API key and internet connection
- `Token Limit Exceeded`: File content too large for selected model

## 💡 Tips for Best Results

1. **Choose the right model**: GPT-4o for complex analysis, GPT-3.5-turbo for simple tasks
2. **Prepare your data**: Clean and organize files before upload
3. **Use specific prompts**: Custom analysis with specific questions yields better results
4. **Monitor token usage**: Larger files and complex analyses use more tokens
5. **Break down large files**: Split very large files for better processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Review the OpenAI API documentation
3. Create an issue in the repository

## 🔄 Future Enhancements

- [ ] Support for more file types (PPT, HTML, etc.)
- [ ] Batch processing optimization
- [ ] Result export in multiple formats (PDF, HTML)
- [ ] Integration with other AI providers
- [ ] Advanced visualization of insights
- [ ] User authentication and session management