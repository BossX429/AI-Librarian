# Contributing to AI Librarian









First off, thank you for considering contributing to AI Librarian! 









## Ways to Contribute









-  Report bugs




-  Suggest new features




-  Improve documentation




-  Submit pull requests




-  Star the repository









## Reporting Bugs









**Before submitting a bug report:**




- Check the existing issues to avoid duplicates




- Try to reproduce the bug with the latest version









**When reporting a bug, include:**




- Your Windows version




- Python version (`python --version`)




- Steps to reproduce




- Expected vs actual behavior




- Relevant logs from `orchestrator/orchestrator.log`









## Suggesting Features









We love new ideas! When suggesting features:




- Explain the problem you're trying to solve




- Describe your proposed solution




- Consider if it fits the project's scope









## Pull Requests









1. **Fork the repository**




2. **Create a branch** (`git checkout -b feature/amazing-feature`)




3. **Make your changes**




4. **Test thoroughly**




5. **Commit** (`git commit -m 'Add amazing feature'`)




6. **Push** (`git push origin feature/amazing-feature`)




7. **Open a Pull Request**









### Pull Request Guidelines









- Follow the existing code style




- Add comments for complex logic




- Update documentation if needed




- Test on Windows 11




- Keep changes focused (one feature per PR)









## Code Style









- **Python:** Follow PEP 8




- **Comments:** Use docstrings for functions




- **Naming:** Use descriptive variable names




- **Formatting:** 4 spaces for indentation









## Testing









Before submitting:




- Test the autonomous mode




- Verify logger captures conversations




- Check compressor reduces file sizes




- Ensure curator updates database




- Test query tools return correct results









## Development Setup









```bash




# Clone your fork




git clone https://github.com/YOUR_USERNAME/AI-Librarian.git




cd AI-Librarian









# Install in development mode




# (No dependencies needed! Uses Python standard library)









# Test manually




cd logger




python claude_desktop_logger.py









# Test compressor




cd ../compressor




python delta_compressor.py compress









# Test curator




cd ../curator  




python claude_curator.py









# Test query tools




cd ../query_tools




python librarian_query.py search "test" 5




```









## Areas That Need Help









-  Mobile app for search




-  Web dashboard




-  Semantic search with embeddings




-  Analytics and insights




-  Linux support




-  macOS support




-  Multi-language UI




-  More documentation









## Questions?









Feel free to open an issue with your question. We're here to help!









## Code of Conduct









- Be respectful and inclusive




- Welcome newcomers




- Focus on constructive feedback




- Help others learn









## License









By contributing, you agree that your contributions will be licensed under the MIT License.









---









**Thank you for making AI Librarian better!** 




