document.addEventListener('DOMContentLoaded', () => {
    const scrollIndicator = document.getElementById('scrollDown');
    const learnMoreButton = document.querySelector('.learn-more-btn');
    const firstInfoSection = document.getElementById('about'); 

    const scrollToSection = (event) => {
        if (event) event.preventDefault(); 
        if (firstInfoSection) {
            window.scrollTo({
                top: firstInfoSection.offsetTop,
                behavior: 'smooth' 
            });
        }
    };

    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', scrollToSection);
    }
    
    if (learnMoreButton) {
        learnMoreButton.addEventListener('click', scrollToSection);
    }

    const mainPanel = document.getElementById('main-panel');
    
    if (mainPanel) {
        const toSignInButton = document.getElementById('toSignIn'); 
        const toSignUpButton = document.getElementById('toSignUp'); 
        
        if (toSignInButton) {
            toSignInButton.addEventListener('click', () => {
                mainPanel.classList.add('right-panel-active'); 
            });
        }

        if (toSignUpButton) {
            toSignUpButton.addEventListener('click', () => {
                mainPanel.classList.remove('right-panel-active');
            });
        }
    }
});